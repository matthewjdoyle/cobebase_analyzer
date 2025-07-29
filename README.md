# Codebase Analyzer v2.0

A comprehensive, modular command-line tool for analyzing codebases with detailed metrics, insights, and visualizations.

## 🚀 New in v2.0

- **Modular Architecture**: Completely refactored with separate modules for core analysis, reporting, exporting, and CLI
- **Extensible Design**: Plugin system for custom reporters and exporters
- **Type Safety**: Full type hints and Pydantic models for data validation
- **Enhanced Configuration**: Comprehensive configuration management with validation
- **Better Error Handling**: Robust error handling and logging throughout
- **Performance Improvements**: Optimized analysis algorithms and progress tracking
- **Multiple Export Formats**: JSON, CSV, and text export options
- **Rich Terminal Output**: Beautiful, interactive terminal interface

## ✨ Features

- **Project Structure Analysis**: Visualize folder hierarchy with per-file statistics
- **File Metrics**: Count files, lines of code, and file sizes with detailed breakdowns
- **Language Detection**: Identify programming languages and file types automatically
- **Code Statistics**: Lines of code, comments, blank lines per file type
- **Size Analysis**: File and directory size breakdowns with human-readable formatting
- **Complexity Metrics**: Basic complexity analysis with configurable thresholds
- **Export Options**: Generate reports in JSON, CSV, and text formats
- **Interactive Mode**: Explore codebase interactively with real-time commands
- **Configuration Management**: Flexible configuration system with validation
- **Progress Tracking**: Real-time progress indicators for large analyses
- **Plugin System**: Extensible architecture for custom reporters and exporters

## 🏗️ Architecture

The project is organized into modular components:

```
src/cobebase_analyzer/
├── core/           # Core analysis functionality
│   ├── analyzer.py # Main analyzer class
│   ├── config.py   # Configuration management
│   └── models.py   # Data models and types
├── reporters/      # Report generation
│   ├── base.py     # Base reporter interface
│   ├── rich_reporter.py    # Rich terminal output
│   └── text_reporter.py    # Plain text output
├── exporters/      # Data export functionality
│   ├── base.py     # Base exporter interface
│   ├── json_exporter.py    # JSON export
│   ├── csv_exporter.py     # CSV export
│   └── txt_exporter.py     # Text export
├── cli/            # Command-line interface
│   └── main.py     # Click-based CLI
├── utils/          # Utility functions
│   └── logger.py   # Logging utilities
└── plugins/        # Plugin system (future)
```

## 📦 Installation

### From Source

1. Clone this repository:
```bash
git clone https://github.com/matthewjdoyle/codebase_analyzer
cd cobebase_analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install in development mode:
```bash
pip install -e .
```

### Development Installation

For development with all tools:
```bash
pip install -e ".[dev]"
```

## 🎯 Usage

### Basic Analysis

```bash
# Analyze current directory
cobebase-analyzer analyze .

# Analyze specific directory
cobebase-analyzer analyze /path/to/your/project

# Quick statistics overview
cobebase-analyzer stats /path/to/your/project
```

### Detailed Analysis

```bash
# Full analysis with detailed metrics
cobebase-analyzer analyze /path/to/your/project --detailed

# Export results to JSON
cobebase-analyzer analyze /path/to/your/project --detailed --export json

# Export results to CSV
cobebase-analyzer analyze /path/to/your/project --export csv
```

### Project Structure Visualization

```bash
# Show project structure as tree
cobebase-analyzer structure /path/to/your/project

# Show deeper structure (up to 5 levels)
cobebase-analyzer structure /path/to/your/project --max-depth 5
```

### Interactive Mode

```bash
# Start interactive exploration
cobebase-analyzer interactive /path/to/your/project
```

### Configuration Management

```bash
# Create default configuration
cobebase-analyzer config

# Create configuration in specific location
cobebase-analyzer config --config-file ./my_config.json
```

### Export Results

```bash
# Export to JSON
cobebase-analyzer export /path/to/project --format json

# Export to CSV with custom output path
cobebase-analyzer export /path/to/project --format csv --output ./results.csv
```

## 🔧 Configuration

The tool uses a comprehensive configuration system with Pydantic validation:

```json
{
  "max_file_size_mb": 100,
  "max_depth": null,
  "follow_symlinks": false,
  "include_hidden": false,
  "show_progress": true,
  "color_output": true,
  "detailed_by_default": false,
  "text_file_extensions": [".py", ".js", ".java", ...],
  "binary_extensions": [".exe", ".dll", ".so", ...],
  "comment_patterns": {
    "Python": {"single": "#", "multi_start": "\"\"\"", "multi_end": "\"\"\""},
    "JavaScript": {"single": "//", "multi_start": "/*", "multi_end": "*/"}
  },
  "complexity_metrics": {
    "enabled": true,
    "max_function_length": 50,
    "max_class_length": 500
  },
  "export_settings": {
    "formats": ["json", "csv", "txt"],
    "directory": "reports",
    "include_timestamp": true
  },
  "performance": {
    "parallel_processing": false,
    "max_workers": 4,
    "chunk_size": 1000
  }
}
```

## 📊 Output Examples

### Rich Terminal Output

```
📊 Codebase Analysis Summary
╭─────────────────────┬─────────╮
│ Metric              │ Value   │
├─────────────────────┼─────────┤
│ Total Files         │ 15      │
│ Total Directories   │ 1       │
│ Total Lines of Code │ 1,857   │
│ Total Size          │ 0.06 MB │
│ Unique File Types   │ 3       │
│ Average File Size   │ 4.2 KB  │
│ Average Lines/File  │ 123.8   │
╰─────────────────────┴─────────╯

📁 File Types Breakdown
╭───────────┬───────┬───────┬───────────┬────────────╮
│ File Type │ Count │ Lines │ Size (MB) │ Percentage │
├───────────┼───────┼───────┼───────────┼────────────┤
│ Python    │ 5     │ 1,420 │ 0.05      │ 33.3%      │
│ Markdown  │ 2     │ 268   │ 0.01      │ 13.3%      │
│ Text      │ 6     │ 22    │ 0.00      │ 40.0%      │
╰───────────┴───────┴───────┴───────────┴────────────╯
```

## 🔌 Extending the Tool

### Creating Custom Reporters

```python
from cobebase_analyzer.reporters.base import BaseReporter
from cobebase_analyzer.core.models import AnalysisResult

class CustomReporter(BaseReporter):
    def generate_report(self, result: AnalysisResult, detailed: bool = False) -> str:
        # Your custom report generation logic
        return "Custom report content"
    
    def display_report(self, result: AnalysisResult, detailed: bool = False) -> None:
        # Your custom display logic
        print(self.generate_report(result, detailed))

# Register your reporter
from cobebase_analyzer.reporters.base import reporter_registry
reporter_registry.register('custom', CustomReporter)
```

### Creating Custom Exporters

```python
from cobebase_analyzer.exporters.base import BaseExporter
from cobebase_analyzer.core.models import AnalysisResult

class CustomExporter(BaseExporter):
    def export(self, result: AnalysisResult, output_path: str) -> None:
        # Your custom export logic
        pass
    
    def get_supported_formats(self) -> list:
        return ['custom']

# Register your exporter
from cobebase_analyzer.exporters.base import exporter_registry
exporter_registry.register('custom', CustomExporter)
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cobebase_analyzer

# Run specific test file
pytest tests/test_analyzer.py
```

## 📝 Development

### Code Quality

```bash
# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

### Building

```bash
# Build package
python setup.py sdist bdist_wheel

# Install in development mode
pip install -e .
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: [README.md](README.md)
- **Issues**: [GitHub Issues](https://github.com/matthewjdoyle/codebase_analyzer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/matthewjdoyle/codebase_analyzer/discussions)

## 🔄 Migration from v1.0

The v2.0 release includes breaking changes for better modularity:

- **New Package Structure**: The tool is now organized in `src/cobebase_analyzer/`
- **Updated CLI**: New command structure with better organization
- **Configuration Changes**: New configuration format with validation
- **API Changes**: Updated import paths and class interfaces

For migration help, see the [Migration Guide](MIGRATION.md).

