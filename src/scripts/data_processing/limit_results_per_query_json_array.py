import json

INPUT_FILE = "data/processed/merged_filtered_results_30.jsonl"
OUTPUT_FILE = "data/results/merged_filtered_results_limited10.json"
MAX_RESULTS = 10


# Read .jsonl file line by line
data = []
with open(INPUT_FILE, "r", encoding="utf-8") as infile:
    for line in infile:
        line = line.strip()
        if line:
            data.append(json.loads(line))

for entry in data:
    if 'solr_results' in entry and isinstance(entry['solr_results'], list):
        entry['solr_results'] = entry['solr_results'][:MAX_RESULTS]
    if 'maps_results' in entry and isinstance(entry['maps_results'], list):
        entry['maps_results'] = entry['maps_results'][:MAX_RESULTS]

with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=2)

print(f"Done. Limited results saved to {OUTPUT_FILE}")
