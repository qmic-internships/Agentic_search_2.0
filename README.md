# Agentic Search Evaluation Pipeline

## Overview

This project is focused on evaluating and improving the quality of our search API by comparing it directly with Google Maps Autocomplete. The process involves cleaning a large set of real user queries, fetching results from both our API and Google Maps using the same parameters, and then running a detailed evaluation to find weaknesses in our data, ranking, and algorithms.

## Workflow

### 1. Data Preparation

- **Source:** We start with a large dataset (`Analytics.json`) containing over 10,000 real user queries.
- **Cleaning:** Duplicate queries are removed so that each query is unique.
- **Keyword Selection:** We extract representative keywords to avoid repetitive or overly long queries, focusing on meaningful and distinct search intents.

### 2. Query Standardization

- **Consistent Lat/Lng:** To ensure a fair comparison, the same latitude and longitude are used for every query when fetching results from both our API and Google Maps Autocomplete. This removes location bias and sets a clear baseline for evaluation.

### 3. Data Fetching

- **Dual API Fetch:** For each standardized query, results are fetched from both our Search API (Solr) and Google Maps Autocomplete API.
- **Parameter Matching:** Both APIs receive the same query text and location parameters.

### 4. Merging & Filtering

- **Result Merging:** The results from both APIs are merged for each query.
- **Filtering:** Only the most relevant parameters (like POI name, container/location, etc.) are kept to focus the evaluation on meaningful output.

### 5. Evaluation

- **Automated Judging:** The cleaned and merged results are evaluated using the deepeval framework and a large language model (Cerebras via LiteLLM).
- **Holistic Metrics:** The evaluation looks at coverage of key results, precision and noise, ranking quality, and overall user satisfaction.
- **Scoring:** Each query’s results are scored and explained by the LLM, providing both quantitative and qualitative feedback.

### 6. Analysis & Improvement

- **Diagnosis:** The evaluation helps determine whether issues are caused by the underlying data (like missing or irrelevant results) or by the search algorithm (like poor ranking or noisy results).
- **Iteration:** Insights from the evaluation are used to improve data cleaning, query formulation, and search ranking logic.

## Goals

- Identify where our API underperforms compared to Google Maps (missing results, poor ranking, irrelevant suggestions).
- Use LLM-based metrics to track improvements as the search system is refined.
- Distinguish between problems caused by data quality and those caused by search logic or ranking.

## How to Run

1. Clean and deduplicate queries, extract representative keywords.
2. Use the provided scripts to fetch results from both APIs for all queries, using consistent lat/lng.
3. Merge and clean the results for fair comparison.
4. Run the evaluation pipeline using deepeval and the LLM judge.
5. Review the scores and reasoning to guide further improvements.

## Why This Matters

A reliable and user-focused search experience is important for our product. By systematically comparing our API to Google Maps and using LLMs for detailed evaluation, we can find weaknesses and make targeted improvements. This helps us deliver more relevant, accurate, and satisfying search results to our users.
