"""
Codebase Analyzer - A comprehensive tool for analyzing codebases

A modular, extensible codebase analysis tool that provides detailed metrics,
insights, and visualizations for software projects.
"""

__version__ = "2.0.0"
__author__ = "Codebase Analyzer Team"
__email__ = "support@codebase-analyzer.com"

from .core.analyzer import CodebaseAnalyzer
from .core.config import Config, load_config, save_config
from .core.models import AnalysisResult, FileInfo, ProjectStats
from .cli.main import cli
from .reporters.base import BaseReporter
from .reporters.rich_reporter import RichReporter
from .reporters.text_reporter import TextReporter
from .exporters.base import BaseExporter
from .exporters.json_exporter import JSONExporter
from .exporters.csv_exporter import CSVExporter
from .exporters.txt_exporter import TextExporter

__all__ = [
    # Core classes
    "CodebaseAnalyzer",
    "Config",
    "AnalysisResult",
    "FileInfo", 
    "ProjectStats",
    
    # CLI
    "cli",
    
    # Reporters
    "BaseReporter",
    "RichReporter", 
    "TextReporter",
    
    # Exporters
    "BaseExporter",
    "JSONExporter",
    "CSVExporter",
    "TextExporter",
    
    # Configuration
    "load_config",
    "save_config",
    
    # Version
    "__version__",
]