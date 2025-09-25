# 🚀 Agentic Search Evaluation Pipeline

A simplified, one-command evaluation system that compares your search API against Google Maps to identify improvement opportunities.

## 🎯 Quick Start

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
python run_pipeline.py --phase dashboard  # Dashboard only
```

### Setup Commands
```bash
python setup.py install      # Full installation
python setup.py check-deps   # Check dependencies only
python setup.py show-info    # Show project info
python setup.py diagnostics  # Run diagnostics
```

## 🔄 Pipeline Phases

### Phase 1: Data Preparation
- Extracts keywords from `data/Analytics.json`
- Removes duplicates and selects representative samples
- Creates optimized keyword lists for evaluation

### Phase 2: API Fetching
- Fetches results from both your Solr API and Google Places
- Uses consistent location parameters for fair comparison
- Stores raw results for analysis

### Phase 3: LLM Evaluation
- Uses Cerebras Llama-3.3-70B model for intelligent evaluation
- Compares results on coverage, precision, and ranking
- Generates detailed reasoning for each comparison

### Phase 4: Dashboard
- Interactive visualization of results
- Filter and analyze evaluation outcomes
- Export reports and insights

## 📊 Key Features

- **One-Command Execution**: Run the entire pipeline with a single command
- **Modular Design**: Run individual phases for development/debugging
- **Smart Caching**: Skips completed phases when data exists
- **Error Handling**: Robust error handling with clear status messages
- **Progress Tracking**: Real-time progress updates and status reporting
- **Flexible Configuration**: Easy to modify parameters and settings

## 📁 Project Structure

```
agentic-search/
├── run_pipeline.py          # 🎯 Main pipeline runner
├── setup.py                 # 🔧 Setup and installation
├── data/
│   ├── Analytics.json       # 📊 Raw analytics data
│   ├── keywords/            # 📝 Processed keyword files
│   ├── processed/           # 🔄 Merged API results
│   └── results/             # 📈 Final evaluation results
├── src/
│   ├── core/               # 🧠 Core evaluation logic
│   └── scripts/            # 🔧 Individual pipeline scripts
└── config.json             # ⚙️ Configuration settings
```

## 🎉 What You Get

After running the pipeline, you'll have:

1. **Evaluation Results** (`data/results/evaluation_results.csv`)
   - Quantitative scores (0.0-10.0) for each query
   - Detailed reasoning explaining the score
   - Comparison between your API and Google Maps

2. **Performance Insights**
   - Coverage analysis (did you return relevant results?)
   - Precision analysis (how much noise in results?)
   - Ranking analysis (are best results ranked highly?)

3. **Interactive Dashboard**
   - Visualize results with charts and filters
   - Export reports for stakeholders
   - Drill down into specific queries

## 🔧 Configuration

Edit `config.json` to customize:
- API endpoints and timeouts
- Evaluation parameters
- Processing settings
- Output directories

## 🐛 Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   python setup.py check-deps
   ```

2. **Path Errors**
   - Ensure you're running from the project root
   - Check that `data/Analytics.json` exists

3. **API Key Issues**
   - Edit `.env` file with your API keys
   - Check `CEREBRAS_API_KEY` for evaluation

4. **Permission Errors**
   - Ensure write permissions in project directory
   - Check antivirus/firewall settings

### Getting Help

```bash
python run_pipeline.py --help    # Show pipeline help
python setup.py show-info        # Show project information
```

## 🚀 Advanced Usage

### Custom Evaluation Parameters
```bash
# Set custom environment variables
export EVAL_SIM_THRESHOLD=0.8
export EVAL_VERBOSE=1
python run_pipeline.py --phase eval
```

### Development Mode
```bash
# Skip dependency checks for faster iteration
python run_pipeline.py --skip-deps --phase data
```

### Batch Processing
```bash
# Process larger datasets
python -m src.scripts.api_fetching.fetch_autocomplete --source both --range 0 1000
```

---

**Happy Evaluating! 🎯**
