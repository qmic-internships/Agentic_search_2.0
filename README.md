# 🚀 Agentic Search Evaluation Pipeline

A powerful, automated system that evaluates your search API against Google Maps to identify improvement opportunities and track performance over time.

## 🎯 Overview

This project evaluates and improves search API quality by comparing it directly with Google Maps Autocomplete. The system processes real user queries, fetches results from both APIs using identical parameters, and uses advanced LLM evaluation to provide detailed performance analysis.

### ✨ Key Features

- **🔄 One-Command Execution**: Run the entire pipeline with a single command
- **🤖 AI-Powered Evaluation**: Uses Cerebras Llama-3.3-70B for intelligent scoring
- **📊 Comprehensive Metrics**: Precision, coverage, ranking, and holistic quality scores
- **🎨 Interactive Dashboard**: Visualize results with charts and filters
- **⚡ Smart Caching**: Skips completed phases automatically
- **🛡️ Robust Error Handling**: Continues processing even with partial failures

## 🚀 Quick Start

### 1. Install Dependencies
```bash
python setup.py install
```

### 2. Run Complete Pipeline
```bash
python run_pipeline.py
```

### 3. View Results
```bash
python run_pipeline.py --phase dashboard
```

## 📋 Available Commands

### Complete Pipeline
```bash
python run_pipeline.py                    # Run everything
```

### Individual Phases
```bash
python run_pipeline.py --phase data       # Data preparation only
python run_pipeline.py --phase api        # API fetching only
python run_pipeline.py --phase eval       # Evaluation only
python run_pipeline.py --phase dashboard  # Launch dashboard only
```

### Setup Commands
```bash
python setup.py install      # Full installation
python setup.py check-deps   # Check dependencies only
python setup.py show-info    # Show project information
python setup.py diagnostics  # Run system diagnostics
```

## 🔄 Pipeline Workflow

### Phase 1: Data Preparation 📊
- **Input**: `data/Analytics.json` (10,000+ real user queries)
- **Process**: Clean, deduplicate, and select representative keywords
- **Output**: Optimized keyword files for evaluation
- **Duration**: ~30 seconds

### Phase 2: API Fetching 🌐
- **Input**: Representative keywords with consistent lat/lng
- **Process**: Fetch results from both your Solr API and Google Places
- **Output**: Raw API comparison data
- **Duration**: 5-15 minutes (varies by API response times)

### Phase 3: LLM Evaluation 🧠
- **Input**: Merged API results
- **Process**: AI-powered analysis using Cerebras Llama-3.3-70B
- **Output**: Detailed evaluation scores and reasoning
- **Duration**: 10-30 minutes (depends on query count)

### Phase 4: Dashboard 📊
- **Input**: Evaluation results
- **Process**: Interactive visualization and analysis
- **Output**: Web dashboard at `http://localhost:8501`
- **Duration**: Starts immediately

## 📊 Evaluation Metrics

### Quantitative Metrics
- **Precision Ratio**: How many of your results are relevant?
- **Mean Reciprocal Rank (MRR)**: How highly are good results ranked?
- **Coverage**: How many Google Places results does your API find?

### Qualitative Metrics
- **Holistic AI Score**: Overall quality assessment (0.0-10.0)
- **Detailed Reasoning**: Specific explanations for each score
- **Improvement Areas**: Targeted recommendations

## 📁 Project Structure

```
agentic-search/
├── run_pipeline.py          # 🎯 Main pipeline runner
├── setup.py                 # 🔧 Installation and setup
├── README.md                # 📖 This file
├── PIPELINE_README.md       # 📋 Detailed pipeline documentation
├── data/
│   ├── Analytics.json       # 📊 Source analytics data
│   ├── keywords/            # 📝 Processed keyword files
│   ├── processed/           # 🔄 Merged API results
│   └── results/             # 📈 Final evaluation results
├── src/
│   ├── core/               # 🧠 Core evaluation logic
│   └── scripts/            # 🔧 Individual pipeline scripts
├── config.json             # ⚙️ Configuration settings
└── requirements.txt        # 📦 Python dependencies
```

## 🎉 What You Get

### Evaluation Results (`data/results/evaluation_results.csv`)
```csv
query,score,reasoning
"Al Mirqab mall",2.5,"The primary POI names are completely different, with 'The Gate Mall' in the actual output and 'Al Mirqab Mall' in the expected output..."
"Al Noor petrol station",4.2,"Results show good coverage but location accuracy needs improvement..."
```

### Performance Insights
- **Coverage Analysis**: Identifies missing relevant results
- **Precision Analysis**: Detects noise and irrelevant suggestions
- **Ranking Analysis**: Evaluates result ordering quality
- **Context Understanding**: Assesses location and qualifier handling

### Interactive Dashboard
- 📊 Charts and visualizations of evaluation results
- 🔍 Filter and search through individual queries
- 📈 Export reports for stakeholders
- 🎯 Drill-down analysis of specific issues

## 🔧 Configuration

Edit `config.json` to customize:
- API endpoints and timeouts
- Evaluation parameters (thresholds, models)
- Processing settings (batch sizes, file paths)
- Output directories and formats

## 🛠️ Advanced Usage

### Custom Evaluation Parameters
```bash
export EVAL_SIM_THRESHOLD=0.8
export EVAL_VERBOSE=1
python run_pipeline.py --phase eval
```

### Development Mode
```bash
python run_pipeline.py --skip-deps --phase data
```

### Batch Processing
```bash
python -m src.scripts.api_fetching.fetch_autocomplete --source both --range 0 1000
```

## 🐛 Troubleshooting

### Common Issues

**Missing Dependencies:**
```bash
python setup.py check-deps
pip install -r requirements.txt
```

**Path Errors:**
- Ensure you're running from project root
- Check that `data/Analytics.json` exists

**API Issues:**
- Verify API keys in `.env` file
- Check `CEREBRAS_API_KEY` for evaluation

**Permission Errors:**
- Ensure write permissions in project directory
- Check antivirus/firewall settings

### Getting Help
```bash
python run_pipeline.py --help        # Pipeline help
python setup.py show-info            # Project information
python setup.py diagnostics          # System diagnostics
```

## 🎯 Why This Matters

A reliable search experience is crucial for user satisfaction. This system:

- **Identifies Weaknesses**: Pinpoints specific areas for improvement
- **Tracks Progress**: Monitors improvements over time
- **Guides Development**: Provides data-driven insights for prioritization
- **Benchmarks Performance**: Compares against industry standards (Google Maps)
- **Accelerates Iteration**: Speeds up the development cycle with automated evaluation

## 📚 Additional Resources

- [Pipeline Documentation](PIPELINE_README.md) - Detailed technical documentation
- [Configuration Guide](config.json) - Advanced configuration options
- [API Reference](src/core/) - Core evaluation logic documentation
