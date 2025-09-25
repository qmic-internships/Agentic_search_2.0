#!/usr/bin/env python3
"""
Agentic Search Evaluation Pipeline - Single Command Runner
=======================================================

This script consolidates the entire workflow into a single command.
Run the complete pipeline or individual phases with simple commands.

Usage:
    python run_pipeline.py                    # Run complete pipeline
    python run_pipeline.py --help           # Show help
    python run_pipeline.py --phase data     # Run only data preparation
    python run_pipeline.py --phase api      # Run only API fetching
    python run_pipeline.py --phase eval     # Run only evaluation
    python run_pipeline.py --phase dashboard # Launch dashboard only

Author: Agentic Search Team
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
import time
from typing import List, Optional

class PipelineRunner:
    """Main pipeline runner class."""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.phases = {
            'data': self.run_data_preparation,
            'api': self.run_api_fetching,
            'eval': self.run_evaluation,
            'dashboard': self.run_dashboard,
            'full': self.run_full_pipeline
        }

    def run_command(self, cmd: str, description: str, cwd: Optional[str] = None) -> bool:
        """Run a command with status updates."""
        print(f"\n{'='*60}")
        print(f"🚀 {description}")
        print(f"{'='*60}")
        print(f"Command: {cmd}")

        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd or self.project_root,
                check=True,
                capture_output=False,
                text=True
            )
            print(f"✅ {description} completed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed with exit code {e.returncode}")
            print(f"Error: {e.stderr}")
            return False
        except Exception as e:
            print(f"❌ {description} failed with error: {str(e)}")
            return False

    def check_dependencies(self) -> bool:
        """Check if required dependencies are installed."""
        print("🔍 Checking dependencies...")

        required_modules = [
            'requests', 'pandas', 'numpy', 'plotly', 'streamlit',
            'tqdm', 'python-dotenv', 'deepeval', 'litellm'
        ]

        missing = []
        for module in required_modules:
            try:
                __import__(module)
                print(f"  ✅ {module}")
            except ImportError:
                missing.append(module)
                print(f"  ❌ {module}")

        if missing:
            print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
            print("📦 Install with: pip install -r requirements.txt")
            return False

        print("✅ All dependencies are installed!")
        return True

    def run_data_preparation(self) -> bool:
        """Run data preparation phase."""
        print("\n📊 PHASE 1: Data Preparation")
        print("=" * 40)

        steps = [
            ("python src/scripts/data_processing/extract_and_sort_keywords.py",
             "Extracting and sorting keywords from Analytics.json"),

            ("python src/scripts/data_processing/remove_duplicates.py",
             "Removing duplicate keywords"),

            ("python src/scripts/data_processing/select_representative_keywords.py",
             "Selecting representative keywords for evaluation")
        ]

        success = True
        for cmd, desc in steps:
            if not self.run_command(cmd, desc):
                success = False

        if success:
            print("\n✅ Data preparation completed successfully!")
            self.show_data_stats()

        return success

    def show_data_stats(self):
        """Show statistics about processed data."""
        keywords_dir = self.project_root / "data" / "keywords"
        if keywords_dir.exists():
            files = list(keywords_dir.glob("*.csv"))
            print(f"📁 Generated {len(files)} keyword files:")
            for file in sorted(files):
                size = file.stat().st_size
                print(f"   • {file.name}: {size:,} bytes")

    def run_api_fetching(self) -> bool:
        """Run API fetching phase."""
        print("\n🌐 PHASE 2: API Data Fetching")
        print("=" * 40)

        # Check if we have existing data
        raw_dir = self.project_root / "raw"
        if raw_dir.exists() and list(raw_dir.glob("*.jsonl")):
            print("📋 Found existing API results, skipping fetch...")
            return True

        # Run API fetching with module syntax
        cmd = "python -m src.scripts.api_fetching.fetch_autocomplete --source both --range 0 100 --lat 25.3246603 --lng 51.4382779"
        success = self.run_command(cmd, "Fetching API results from Solr and Google Places")

        if success:
            print("\n✅ API fetching completed!")
            self.show_raw_data_stats()

        return success

    def show_raw_data_stats(self):
        """Show statistics about raw API data."""
        raw_dir = self.project_root / "raw"
        if raw_dir.exists():
            files = list(raw_dir.glob("*.jsonl"))
            print(f"📁 Generated {len(files)} raw data files:")
            for file in sorted(files):
                size = file.stat().st_size
                print(f"   • {file.name}: {size:,} bytes")

    def run_evaluation(self) -> bool:
        """Run evaluation phase."""
        print("\n🧠 PHASE 3: LLM Evaluation")
        print("=" * 40)

        # Check if we have processed data
        processed_dir = self.project_root / "data" / "processed"
        if processed_dir.exists() and list(processed_dir.glob("*.jsonl")):
            print("📋 Found existing processed data, checking evaluation status...")

            # Check if evaluation already exists
            results_dir = self.project_root / "data" / "results"
            if results_dir.exists() and (results_dir / "evaluation_results.csv").exists():
                print("📋 Found existing evaluation results, skipping evaluation...")
                return True

        # Run merge and filter first if needed
        merge_cmd = "python -m src.scripts.api_fetching.merge_and_filter_results"
        if not self.run_command(merge_cmd, "Merging and filtering API results"):
            return False

        # Run evaluation
        eval_cmd = "python -m src.scripts.evaluation.run_evaluation_5"
        success = self.run_command(eval_cmd, "Running LLM-based evaluation")

        if success:
            print("\n✅ Evaluation completed!")
            self.show_evaluation_stats()

        return success

    def show_evaluation_stats(self):
        """Show statistics about evaluation results."""
        results_dir = self.project_root / "data" / "results"
        if results_dir.exists():
            files = list(results_dir.glob("*.csv")) + list(results_dir.glob("*.jsonl"))
            print(f"📁 Generated {len(files)} evaluation files:")
            for file in sorted(files):
                size = file.stat().st_size
                print(f"   • {file.name}: {size:,} bytes")

    def run_dashboard(self) -> bool:
        """Launch the dashboard."""
        print("\n📊 PHASE 4: Launch Dashboard")
        print("=" * 40)

        cmd = "python run_dashboard.py"
        success = self.run_command(cmd, "Starting Streamlit dashboard")

        if success:
            print("\n🎉 Dashboard is running!")
            print("📱 Open your browser and go to: http://localhost:8501")

        return success

    def run_full_pipeline(self) -> bool:
        """Run the complete pipeline."""
        print("🚀 RUNNING COMPLETE AGENTIC SEARCH EVALUATION PIPELINE")
        print("=" * 60)

        phases = [
            ("Data Preparation", self.run_data_preparation),
            ("API Fetching", self.run_api_fetching),
            ("Evaluation", self.run_evaluation),
            ("Dashboard", self.run_dashboard)
        ]

        overall_success = True
        for phase_name, phase_func in phases:
            print(f"\n{'='*60}")
            print(f"🎯 Starting {phase_name}...")
            print(f"{'='*60}")

            if not phase_func():
                print(f"❌ {phase_name} failed!")
                overall_success = False
                break

            # Small delay between phases
            time.sleep(1)

        if overall_success:
            print(f"\n{'='*60}")
            print("🎉 COMPLETE PIPELINE FINISHED SUCCESSFULLY!")
            print(f"{'='*60}")
            print("📊 Check your results in: data/results/evaluation_results.csv")
            print("📱 Launch dashboard anytime with: python run_pipeline.py --phase dashboard")
        else:
            print(f"\n{'='*60}")
            print("⚠️  PIPELINE COMPLETED WITH ERRORS")
            print("🔧 Check the error messages above and fix issues before retrying")
            print(f"{'='*60}")

        return overall_success

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Agentic Search Evaluation Pipeline Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_pipeline.py                    # Run complete pipeline
  python run_pipeline.py --phase data       # Run only data preparation
  python run_pipeline.py --phase api        # Run only API fetching
  python run_pipeline.py --phase eval       # Run only evaluation
  python run_pipeline.py --phase dashboard  # Launch dashboard only
  python run_pipeline.py --skip-deps        # Skip dependency check
        """
    )

    parser.add_argument(
        '--phase',
        choices=['data', 'api', 'eval', 'dashboard', 'full'],
        default='full',
        help='Pipeline phase to run (default: full pipeline)'
    )

    parser.add_argument(
        '--skip-deps',
        action='store_true',
        help='Skip dependency check'
    )

    args = parser.parse_args()

    # Create pipeline runner
    runner = PipelineRunner()

    # Check dependencies unless skipped
    if not args.skip_deps:
        if not runner.check_dependencies():
            print("\n❌ Cannot continue without required dependencies.")
            print("💡 Run: pip install -r requirements.txt")
            sys.exit(1)

    # Run the requested phase
    success = runner.phases[args.phase]()

    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
