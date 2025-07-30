# Codebase Analyzer

A comprehensive command-line tool for analyzing codebases with detailed metrics, insights, and beautiful visualizations.

## ✨ Features

- **Project Structure Analysis**: Visualize folder hierarchy and organization with per-file statistics
- **File Metrics**: Count files, lines of code, and file sizes
- **Language Detection**: Identify programming languages and file types
- **Code Statistics**: Lines of code, comments, blank lines per file type
- **Size Analysis**: File and directory size breakdowns
- **Complexity Metrics**: Basic complexity analysis
- **Export Options**: Generate reports in various formats (JSON, CSV, TXT)
- **Interactive Mode**: Explore codebase interactively
- **📊 Beautiful Visualizations**: Create stunning matplotlib charts and graphs (NEW!)

## 🆕 New in Version 2.0

- **🏗️ Modular Architecture**: Refactored using best programming practices with separated concerns
- **📊 Matplotlib Visualizations**: Beautiful charts including pie charts, bar charts, and tree maps
- **🎨 Enhanced CLI**: New `--visualize` option and dedicated `visualize` command
- **📋 Improved Code Quality**: Better error handling, type hints, and documentation
- **🚀 Better Performance**: Optimized analysis with cleaner code structure

## Installation

1. Clone this repository:
```bash
git clone https://github.com/matthewjdoyle/codebase_analyzer
cd cobebase_analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make the tool executable:
```bash
python -m pip install -e .
```

## Usage

### Basic Analysis (Default)
```bash
python analyzer.py analyze /path/to/your/codebase
```

### Analysis with Beautiful Visualizations ✨
```bash
python analyzer.py analyze /path/to/your/codebase --visualize
```

### Create Only Visualizations
```bash
python analyzer.py visualize /path/to/your/codebase
```

### Quick Statistics with Visualizations
```bash
python analyzer.py stats /path/to/your/codebase --visualize
```

The default output includes:
- 📊 **Summary Statistics**: Total files, directories, lines of code, and size
- 📁 **File Types Breakdown**: Count, lines, and size by file type
- 🌳 **Project Structure**: Tree view with per-file statistics (type, size, lines)

### Detailed Analysis with Additional Metrics
```bash
python analyzer.py analyze /path/to/your/codebase --detailed
```

The detailed output adds:
- 📏 **Largest Files**: Top 10 largest files by size
- 🔍 **Detailed Metrics**: Code/comment/blank line breakdowns with ratios

### Other Commands
```bash
# Quick statistics overview
python analyzer.py stats /path/to/your/codebase

# Show project structure as tree
python analyzer.py structure /path/to/your/codebase

# Interactive exploration mode
python analyzer.py interactive /path/to/your/codebase
```

### Available Commands

- `analyze`: Perform comprehensive codebase analysis (default: summary + tree)
- `visualize`: Create beautiful matplotlib visualizations of statistics ✨
- `interactive`: Start interactive exploration mode
- `stats`: Quick statistics overview
- `structure`: Show project structure tree

### Options

- `--detailed`: Include additional detailed metrics (largest files, code/comment ratios)
- `--visualize`: Create beautiful matplotlib charts and graphs ✨
- `--export FORMAT`: Export results (json, csv, txt)
- `--ignore PATTERN`: Ignore files/directories matching pattern
- `--max-depth N`: Maximum directory depth to analyze
- `--sort-by FIELD`: Sort results by field (size, lines, name)
- `--output-dir DIR`: Output directory for visualizations
- `--show`: Show visualizations in addition to saving them

## 📊 Visualization Types

The tool creates five types of beautiful visualizations:

1. **File Types Distribution** (Pie Chart): Shows the proportion of different file types
2. **Lines of Code by Type** (Bar Chart): Displays lines of code for each file type
3. **File Size Distribution** (Bar Chart): Shows total file sizes by type
4. **Largest Files** (Horizontal Bar Chart): Top 10 largest files in your codebase
5. **Code Composition** (Stacked Bar Chart): Code, comment, and blank lines breakdown

All visualizations are saved as high-quality PNG files with professional styling.

## 🏗️ Architecture

The codebase has been refactored using best programming practices:

```
cobebase_analyzer/
├── core/               # Core analysis functionality
│   ├── analyzer.py     # Main codebase analyzer
│   └── file_analyzer.py # Individual file analysis
├── reports/            # Reporting and visualization
│   ├── reporter.py     # Report generation and display
│   └── visualizer.py   # Matplotlib visualizations
├── cli/                # Command-line interface
│   └── commands.py     # CLI command implementations
├── utils/              # Utility functions
│   └── file_utils.py   # File type detection and utilities
├── analyzer.py         # Main entry point (backward compatible)
├── config.py          # Configuration settings
└── requirements.txt   # Dependencies
```

### Design Principles Applied:

- **Single Responsibility Principle**: Each module has one clear purpose
- **Open/Closed Principle**: Easy to extend with new visualization types
- **Dependency Inversion**: Abstractions used for different report types
- **Separation of Concerns**: Analysis, reporting, CLI, and utilities are separated
- **Modular Design**: Clean interfaces between components

## Output Examples

### Default Analysis Output
```
📊 Codebase Analysis Summary
╭─────────────────────┬─────────╮
│ Metric              │ Value   │
├─────────────────────┼─────────┤
│ Total Files         │ 15      │
│ Total Directories   │ 1       │
│ Total Lines of Code │ 1,857   │
│ Total Size          │ 0.06 MB │
╰─────────────────────┴─────────╯

📁 File Types Breakdown
╭───────────┬───────┬───────┬───────────╮
│ File Type │ Count │ Lines │ Size (MB) │
├───────────┼───────┼───────┼───────────┤
│ Python    │ 5     │ 1,420 │ 0.05      │
│ Markdown  │ 2     │ 268   │ 0.01      │
│ Text      │ 6     │ 22    │ 0.00      │
╰───────────┴───────┴───────┴───────────╯

🌳 Project Structure with File Statistics
📁 project-name
├── 📄 analyzer.py (Python) - 28.2KB, 662 lines
├── 📄 config.py (Python) - 8.1KB, 201 lines
├── 📄 README.md (Markdown) - 2.2KB, 85 lines
└── 📄 requirements.txt (Text) - 0.1KB, 5 lines
```

## Output

The tool provides:
- Rich terminal output with colors and formatting
- Detailed metrics for each file type
- Project structure visualization with per-file statistics
- Summary statistics
- Exportable reports

## Supported File Types

- Programming languages: Python, JavaScript, TypeScript, Java, C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin
- Web technologies: HTML, CSS, SCSS, SASS, JSX, TSX
- Configuration files: JSON, YAML, TOML, XML, INI
- Documentation: Markdown, RST, TXT
- And many more...

