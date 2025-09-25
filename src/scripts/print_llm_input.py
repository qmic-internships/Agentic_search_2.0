import json
import sys
from typing import Any

def format_poi_list(poi_list, name_key, container_key):
    """
    Formats the top-5 lists and evaluates them using the holistic AI judge.
    """
    if not poi_list:
        return "No results provided."
    return "\n".join([
        f"{i+1}. {r.get(name_key, 'N/A')} ({r.get(container_key, 'N/A')})"
        for i, r in enumerate(poi_list)
    ])

def print_llm_input(data: Any):
    output_json_path = "src/scripts/llm_input.json"
    formatted_blocks = []
    if isinstance(data, list):
        for entry in data:
            query = entry.get("query", "N/A")
            solr_results = entry.get("solr_results", [])
            google_results = entry.get("google_autocomplete_results", [])
            solr_formatted = format_poi_list(solr_results, "solr_poiName", "solr_containerName")
            google_formatted = format_poi_list(google_results, "google_main_text", "google_secondary_text")
            # block = f"Query: {query}\nSolr Results:\n{solr_formatted}\n\nGoogle Autocomplete Results:\n{google_formatted}\n"
            block = f"{solr_formatted}\n{google_formatted}"
            formatted_blocks.append(block)
        formatted = "\n".join(formatted_blocks)
    else:
        formatted = str(data)
    with open(output_json_path, "w", encoding="utf-8") as f:
        f.write(formatted)


def main():
    """
    Usage:
      python printt_llm_input.py
    Or pipe JSON data:
      python printt_llm_input.py
    """
    if not sys.stdin.isatty():
        # Read from stdin
        data = json.load(sys.stdin)
    elif len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        # Default to the provided payload file
        default_path = "data/results/merged_filtered_results_limited.json"
        try:
            with open(default_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Failed to load default payload file '{default_path}': {e}")
            sys.exit(1)
    print_llm_input(data)


if __name__ == "__main__":
    main()
