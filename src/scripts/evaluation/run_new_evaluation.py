import os
import json
from src.core.new_evaluation import evaluate_poi_set

INPUT_PATH = os.path.join("data", "processed", "merged_filtered_results_limited10.json")
OUTPUT_PATH = os.path.join("data", "processed", "poi_evaluated.jsonl")

def extract_google_pois(google_results):
	# Only include POIs that mention Qatar in the text (Qatar-centric filtering)
	pois = []
	for item in google_results:
		if isinstance(item, dict):
			text = item.get("google_place_prediction_text") or item.get("main_text")
			if text and "qatar" in text.lower():
				pois.append(text)
	return pois

def extract_solr_pois(solr_results):
	pois = []
	for item in solr_results:
		if isinstance(item, dict):
			if "solr_name" in item:
				pois.append(item["solr_name"])
			elif "poi_name" in item:
				pois.append(item["poi_name"])
	return pois

def main():
	results = []
	# Detect input format
	if INPUT_PATH.endswith('.jsonl'):
		with open(INPUT_PATH, "r") as f:
			for line in f:
				line = line.strip()
				if line:
					item = json.loads(line)
					query = item.get("query", "")
					google_results = item.get("google_autocomplete_results", [])
					solr_results = item.get("solr_results", [])
					google_pois = extract_google_pois(google_results)
					solr_pois = extract_solr_pois(solr_results)
					eval_result = evaluate_poi_set(query, google_pois, solr_pois)
					item.update(eval_result)
					results.append(item)
	elif INPUT_PATH.endswith('.json'):
		with open(INPUT_PATH, "r") as f:
			data = json.load(f)
			for item in data:
				query = item.get("query", "")
				google_results = item.get("google_autocomplete_results", [])
				solr_results = item.get("solr_results", [])
				google_pois = extract_google_pois(google_results)
				solr_pois = extract_solr_pois(solr_results)
				eval_result = evaluate_poi_set(query, google_pois, solr_pois)
				item.update(eval_result)
				results.append(item)
	else:
		raise ValueError(f"Unsupported input file format: {INPUT_PATH}")

	# Output as .jsonl or .json
	if OUTPUT_PATH.endswith('.jsonl'):
		with open(OUTPUT_PATH, "w") as out:
			for item in results:
				out.write(json.dumps(item, ensure_ascii=False) + "\n")
	elif OUTPUT_PATH.endswith('.json'):
		with open(OUTPUT_PATH, "w") as out:
			json.dump(results, out, ensure_ascii=False, indent=2)
	else:
		raise ValueError(f"Unsupported output file format: {OUTPUT_PATH}")

if __name__ == "__main__":
	main()
