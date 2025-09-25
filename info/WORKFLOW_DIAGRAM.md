# 🔄 Agentic Search 2.0 - Complete Workflow Diagram

## Data Flow Overview

```
📊 ANALYTICS DATA
    ↓
[extract_and_sort_keywords.py]
    ↓
📄 sorted_keywords_with_location.csv
    ↓
[remove_duplicates.py]
    ↓
📄 unique_keywords_with_location.csv
    ↓
[select_representative_keywords.py]
    ↓
📄 uniquerepresentative_keywords_with_location.csv
    ↓
[fetch_autocomplete.py] ──────────────────────────────────────┐
    ↓                                                         │
🌐 SOLR API ──────────────────────────────────────────────────┤
    ↓                                                         │
📄 api_results_solr_{start}_{end}.jsonl ──────────────────────┤
    ↓                                                         │
[merge_and_filter_results.py] ←───────────────────────────────┘
    ↓
📄 merged_filtered_results.jsonl
    ↓
[run_evaluation.py] ──┐
    ↓                 │
📄 advanced_evaluation_report.jsonl ──┤
    ↓                                 │
[run_evaluation_5.py] ────────────────┤
    ↓                                 │
📄 evaluation_report_5.jsonl ────────┤
    ↓                                 │
[run_new_evaluation.py] ──────────────┤
    ↓                                 │
📄 poi_evaluated.jsonl ──────────────┤
    ↓                                 │
[dashboard.py] ←──────────────────────┘
    ↓
🌐 Streamlit Dashboard (localhost:8501)
```

## Phase-by-Phase Breakdown

### Phase 1: Data Preparation
```
Analytics.json
    ↓ extract_and_sort_keywords.py
sorted_keywords_with_location.csv
    ↓ remove_duplicates.py
unique_keywords_with_location.csv
    ↓ select_representative_keywords.py
uniquerepresentative_keywords_with_location.csv
```

### Phase 2: API Fetching
```
uniquerepresentative_keywords_with_location.csv
    ↓ fetch_autocomplete.py
    ├── Solr API → api_results_solr_{start}_{end}.jsonl
    └── Google API → google_autocomplete_results_{start}_{end}.jsonl
```

### Phase 3: Data Processing
```
Raw API Results
    ↓ merge_and_filter_results.py
merged_filtered_results.jsonl
    ↓ limit_results_per_query_json_array.py (optional)
merged_filtered_results_limited10.json
```

### Phase 4: Evaluation (3 Methods)
```
merged_filtered_results.jsonl
    ├── run_evaluation.py → advanced_evaluation_report.jsonl
    ├── run_evaluation_5.py → evaluation_report_5.jsonl
    └── run_new_evaluation.py → poi_evaluated.jsonl
```

### Phase 5: Visualization
```
All Evaluation Reports
    ↓ dashboard.py
Streamlit Dashboard
```

## File Generation Summary

### Input Files (Required)
- `data/Analytics.json` - Source analytics data
- `config.json` - Configuration settings
- `.env` - Environment variables (API keys)

### Generated Files by Category

#### Raw Data
- `raw/api_results_solr_*.jsonl`
- `raw/google_autocomplete_results_*.jsonl`

#### Processed Data
- `data/keywords/sorted_keywords_with_location.csv`
- `data/keywords/unique_sorted_keywords_with_location.csv`
- `data/keywords/unique_keywords_with_location.csv`
- `data/keywords/uniquerepresentative_keywords_with_location.csv`
- `data/processed/merged_filtered_results.jsonl`
- `data/processed/merged_filtered_results_30.jsonl`
- `data/results/merged_filtered_results_limited10.json`

#### Evaluation Reports
- `data/results/advanced_evaluation_report.jsonl`
- `evaluation_report_5.jsonl`
- `data/processed/poi_evaluated.jsonl`

#### Logs
- `logs/` directory (if logging enabled)

## Command Quick Reference

### Complete Pipeline
```bash
# 1. Data preparation
python src/scripts/data_processing/extract_and_sort_keywords.py
python src/scripts/data_processing/remove_duplicates.py
python src/scripts/data_processing/select_representative_keywords.py

# 2. API fetching
python -m src.scripts.api_fetching.fetch_autocomplete --source both --range 0 4430

# 3. Data processing
python src/scripts/api_fetching/merge_and_filter_results.py

# 4. Evaluation
python src/scripts/evaluation/run_evaluation.py

# 5. Visualization
python run_dashboard.py
```

### Quick Test (30 queries)
```bash
python -m src.scripts.api_fetching.fetch_autocomplete --source both --range 0 30
python src/scripts/api_fetching/merge_and_filter_results.py
python src/scripts/evaluation/run_evaluation_5.py
python run_dashboard.py
```

