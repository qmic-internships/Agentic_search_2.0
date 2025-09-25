# src/scripts/evaluation/run_advanced_evaluation.py

import os
import json
import logging
import time
from tqdm import tqdm
from typing import List, Dict, Any
import re
import unicodedata

# Import the single, powerful evaluation function
from src.core.evaluation_5 import evaluate_holistic_search_quality

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


def calculate_quantitative_metrics(solr_list: List[Dict], google_list: List[Dict]) -> Dict[str, Any]:
    """
    Calculates fast, objective metrics (Precision, Coverage, MRR) without LLM calls,
    using string similarity to compare the two result lists.
    """
    
    def _normalize(s: Any) -> str:
        s = str(s or "").lower()
        s = "".join(c for c in unicodedata.normalize("NFKD", s) if unicodedata.category(c) != "Mn")
        return re.sub(r"[^a-z0-9\s]", " ", s).strip()

    def _get_tokens(s: str) -> set:
        return set(_normalize(s).split())

    def jaccard_similarity(set1: set, set2: set) -> float:
        if not set1 and not set2: return 1.0
        if not set1 or not set2: return 0.0
        return len(set1.intersection(set2)) / len(set1.union(set2))

    relevance_threshold = 0.5  # Similarity score needed to be considered a "match"
    
    # --- Precision ---
    # What fraction of Solr results are relevant to *anything* in the Google list?
    relevant_solr_count = 0
    for solr_item in solr_list:
        solr_tokens = _get_tokens(solr_item.get('poi_name'))
        best_sim_for_solr_item = 0
        for google_item in google_list:
            google_tokens = _get_tokens(google_item.get('main_text'))
            best_sim_for_solr_item = max(best_sim_for_solr_item, jaccard_similarity(solr_tokens, google_tokens))
        if best_sim_for_solr_item >= relevance_threshold:
            relevant_solr_count += 1
    precision = relevant_solr_count / len(solr_list) if solr_list else 0

    # --- Coverage & Mean Reciprocal Rank (MRR) ---
    # For each Google result, find its best match in the Solr list.
    reciprocal_ranks = []
    coverage_report = {}
    for google_item in google_list:
        google_tokens = _get_tokens(google_item.get('main_text'))
        best_match = {"score": -1.0, "rank": -1}
        for i, solr_item in enumerate(solr_list):
            solr_tokens = _get_tokens(solr_item.get('poi_name'))
            sim = jaccard_similarity(solr_tokens, google_tokens)
            if sim > best_match["score"]:
                best_match = {"score": sim, "rank": i + 1}
        
        coverage_report[google_item.get('main_text')] = best_match
        if best_match["score"] >= relevance_threshold:
            reciprocal_ranks.append(1.0 / best_match["rank"])
            
    mrr = sum(reciprocal_ranks) / len(google_list) if google_list else 0

    return {
        "precision_ratio": round(precision, 4),
        "mean_reciprocal_rank": round(mrr, 4),
        "coverage_per_google_poi": coverage_report,
    }


def main():
    """Main function to load data, orchestrate the holistic evaluation, and save a detailed report."""
    input_path = os.getenv("EVAL_INPUT_PATH", "data/results/merged_filtered_results_limited.json")
    output_path = os.getenv("EVAL_OUTPUT_PATH", "evaluation_report_5.jsonl")

    logger.info(f"Loading data from: '{input_path}'")
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            records = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Failed to load or parse input file: {e}")
        return

    logger.info(f"Found {len(records)} queries. Starting evaluation...")
    final_reports = []

    # Using 'with' ensures the output file is properly closed even if errors occur.
    with open(output_path, "w", encoding="utf-8") as f_out:
        for record in tqdm(records, desc="Evaluating Queries"):
            query = record.get("query", "Unknown Query")
            solr_list_raw = record.get("solr_results", [])
            google_list_raw = record.get("google_autocomplete_results", [])

            # Format data into a consistent structure for evaluation functions
            solr_list = [{"poi_name": r.get("solr_poiName"), "container": r.get("solr_containerName")} for r in solr_list_raw]
            google_list = [{"main_text": r.get("google_main_text"), "secondary_text": r.get("google_secondary_text")} for r in google_list_raw]

            # 1. Calculate fast, objective quantitative metrics
            quantitative_metrics = calculate_quantitative_metrics(solr_list, google_list)

            # 2. Get the slow, nuanced qualitative AI judgment
            holistic_judgment = evaluate_holistic_search_quality(query, solr_list, google_list)
            
            # Rate limit to be respectful of the API endpoint. Adjust as needed.
            time.sleep(4) 
            
            # 3. Assemble the final, comprehensive report for this query
            report = {
                "query": query,
                "holistic_ai_score": holistic_judgment.get("score"),
                "holistic_ai_reasoning": holistic_judgment.get("reasoning"),
                "quantitative_metrics": quantitative_metrics,
                "source_data": {
                    "solr_count": len(solr_list),
                    "google_count": len(google_list),
                    "solr_top5": solr_list,
                    "google_top5": google_list,
                }
            }
            final_reports.append(report)

            # 4. Write the result for this query to the file immediately
            f_out.write(json.dumps(report, indent=4) + "\n")

    logger.info(f"--- Evaluation Complete ---")
    logger.info(f"Saved detailed evaluation report for {len(final_reports)} queries to '{output_path}'")


if __name__ == "__main__":
    main()