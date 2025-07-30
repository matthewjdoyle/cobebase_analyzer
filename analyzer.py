#!/usr/bin/env python3
"""
Codebase Analyzer - A comprehensive tool for analyzing codebases
Refactored version using modular architecture with matplotlib visualizations
"""

import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import the new modular components
from core.analyzer import CodebaseAnalyzer
from reports.reporter import Reporter
from reports.visualizer import Visualizer
from cli.commands import cli
from utils.file_utils import DEFAULT_IGNORE_PATTERNS


def main():
    """Main entry point"""
    cli()


if __name__ == '__main__':
    main()
    


def main():
    """Main entry point"""
    cli()

if __name__ == '__main__':
    main()