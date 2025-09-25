#!/usr/bin/env python3
"""
Setup script for Agentic Search Evaluation Pipeline
==================================================

Quick setup and installation for the evaluation pipeline.

Usage:
    python setup.py install
    python setup.py check-deps
    python setup.py show-info
"""

import subprocess
import sys
import os
from pathlib import Path

class SetupManager:
    """Handles setup and installation tasks."""

    def __init__(self):
        self.project_root = Path(__file__).parent

    def run_command(self, cmd: str, description: str) -> bool:
        """Run a command with error handling."""
        print(f"🔧 {description}...")
        try:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=False)
            print(f"✅ {description} completed!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed: {e}")
            return False

    def install_dependencies(self) -> bool:
        """Install Python dependencies."""
        print("📦 Installing Python dependencies...")
        return self.run_command("pip install -r requirements.txt", "Installing dependencies")

    def check_environment(self) -> bool:
        """Check environment setup."""
        print("🔍 Checking environment...")

        # Check if .env file exists
        env_file = self.project_root / ".env"
        if not env_file.exists():
            print("⚠️  .env file not found. Creating from template...")
            env_template = self.project_root / ".env.example"
            if env_template.exists():
                import shutil
                shutil.copy(env_template, env_file)
                print("✅ Created .env file from template")
                print("💡 Please edit .env file with your API keys")
            else:
                print("❌ .env.example template not found")
                return False

        # Check required directories
        required_dirs = ["data", "raw", "data/keywords", "data/processed", "data/results"]
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                print(f"📁 Created directory: {dir_path}")

        print("✅ Environment check completed!")
        return True

    def show_info(self):
        """Show project information."""
        print("\n" + "="*60)
        print("🤖 AGENTIC SEARCH EVALUATION PIPELINE")
        print("="*60)
        print("📁 Project Location:", self.project_root)
        print("📄 Main Pipeline:", "run_pipeline.py")
        print("📊 Dashboard:", "run_dashboard.py")
        print("📋 Config:", "config.json")
        print("🔑 Environment:", ".env")
        print("\n📚 Key Files:")
        print("  • data/Analytics.json - Raw analytics data")
        print("  • data/results/evaluation_results.csv - Final results")
        print("  • src/core/evaluation.py - Evaluation logic")
        print("  • src/core/api_client.py - API interfaces")
        print("="*60)

    def run_diagnostics(self) -> bool:
        """Run basic diagnostics."""
        print("🔍 Running diagnostics...")

        # Check Python version
        python_version = sys.version.split()[0]
        print(f"🐍 Python Version: {python_version}")

        # Check key files
        key_files = [
            "requirements.txt",
            "config.json",
            ".env",
            "data/Analytics.json"
        ]

        missing_files = []
        for file_path in key_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                size = full_path.stat().st_size
                print(f"✅ {file_path}: {size:,} bytes")
            else:
                missing_files.append(file_path)
                print(f"❌ {file_path}: Missing")

        if missing_files:
            print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
            return False

        print("✅ Diagnostics completed!")
        return True

def main():
    """Main setup function."""
    if len(sys.argv) < 2:
        print("Usage: python setup.py <command>")
        print("Commands: install, check-deps, show-info, diagnostics")
        sys.exit(1)

    command = sys.argv[1]
    setup = SetupManager()

    if command == "install":
        print("🚀 Starting installation...")

        success = True
        success &= setup.install_dependencies()
        success &= setup.check_environment()
        success &= setup.run_diagnostics()

        if success:
            print("\n🎉 Installation completed successfully!")
            setup.show_info()
        else:
            print("\n❌ Installation failed!")
            sys.exit(1)

    elif command == "check-deps":
        success = setup.install_dependencies()
        sys.exit(0 if success else 1)

    elif command == "show-info":
        setup.show_info()

    elif command == "diagnostics":
        success = setup.run_diagnostics()
        sys.exit(0 if success else 1)

    else:
        print(f"Unknown command: {command}")
        print("Available commands: install, check-deps, show-info, diagnostics")
        sys.exit(1)

if __name__ == "__main__":
    main()
