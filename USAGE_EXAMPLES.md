# Codebase Analyzer - Usage Examples

This document provides practical examples of how to use the Codebase Analyzer tool.

## Basic Usage

### 1. Quick Analysis
```bash
# Analyze current directory
python analyzer.py analyze .

# Analyze specific directory
python analyzer.py analyze /path/to/your/project

# Quick statistics overview
python analyzer.py stats /path/to/your/project
```

### 2. Detailed Analysis
```bash
# Full analysis with detailed metrics
python analyzer.py analyze /path/to/your/project --detailed

# Export results to JSON
python analyzer.py analyze /path/to/your/project --detailed --export json

# Export results to CSV
python analyzer.py analyze /path/to/your/project --export csv
```

### 3. Project Structure Visualization
```bash
# Show project structure as tree
python analyzer.py structure /path/to/your/project

# Show deeper structure (up to 5 levels)
python analyzer.py structure /path/to/your/project --max-depth 5
```

### 4. Interactive Mode
```bash
# Start interactive exploration
python analyzer.py interactive /path/to/your/project
```

## Advanced Usage

### 1. Custom Ignore Patterns
```bash
# Ignore specific patterns
python analyzer.py analyze /path/to/your/project --ignore "*.log" --ignore "temp/*"

# Ignore multiple patterns
python analyzer.py analyze /path/to/your/project --ignore "*.pyc" --ignore "__pycache__" --ignore ".git"
```

### 2. Depth Limiting
```bash
# Analyze only first 3 levels deep
python analyzer.py analyze /path/to/your/project --max-depth 3
```

### 3. Export Options
```bash
# Export to JSON with timestamp
python analyzer.py analyze /path/to/your/project --export json

# Export to CSV for spreadsheet analysis
python analyzer.py analyze /path/to/your/project --export csv

# Export to plain text
python analyzer.py analyze /path/to/your/project --export txt
```

## Real-World Examples

### Example 1: Analyzing a Python Web Application
```bash
# Navigate to your Django/Flask project
cd /path/to/my-web-app

# Get quick overview
python analyzer.py stats .

# Detailed analysis with export
python analyzer.py analyze . --detailed --export json

# Check project structure
python analyzer.py structure . --max-depth 4
```

### Example 2: Analyzing a JavaScript/Node.js Project
```bash
# Navigate to your Node.js project
cd /path/to/my-node-app

# Analyze with custom ignore patterns
python analyzer.py analyze . --ignore "node_modules" --ignore "dist" --ignore "*.min.js"

# Export results for team review
python analyzer.py analyze . --detailed --export csv
```

### Example 3: Comparing Multiple Projects
```bash
# Analyze project A
python analyzer.py analyze /path/to/project-a --export json

# Analyze project B
python analyzer.py analyze /path/to/project-b --export json

# Compare the generated JSON files
```

### Example 4: Continuous Integration
```bash
# In your CI/CD pipeline
python analyzer.py analyze . --export json > analysis_report.json

# Check if codebase size is within limits
python analyzer.py stats . | grep "Total Size"
```

## Interactive Mode Commands

When using interactive mode, you can use these commands:

```
> tree          # Show project structure
> stats         # Show quick statistics
> analyze       # Run full analysis
> quit          # Exit interactive mode
```

## Output Interpretation

### Summary Metrics
- **Total Files**: Number of files analyzed
- **Total Directories**: Number of directories traversed
- **Total Lines of Code**: Total lines across all text files
- **Total Size**: Combined size of all files in MB

### File Types Breakdown
- **File Type**: Programming language or file format
- **Count**: Number of files of this type
- **Lines**: Total lines of code for this type
- **Size**: Combined size of files of this type

### Largest Files
- **File**: Filename
- **Type**: File type/category
- **Size**: File size in KB
- **Lines**: Number of lines in the file

### Detailed Metrics (with --detailed flag)
- **Code Lines**: Actual code lines (excluding comments and blanks)
- **Comment Lines**: Lines containing comments
- **Blank Lines**: Empty lines
- **Comment Ratio**: Percentage of comments vs code

## Tips and Best Practices

1. **Use --detailed for comprehensive analysis**: Provides code/comment/blank line breakdowns
2. **Export results for tracking**: Use JSON/CSV exports to track codebase growth over time
3. **Customize ignore patterns**: Exclude build artifacts, dependencies, and generated files
4. **Limit depth for large projects**: Use --max-depth to avoid analyzing deeply nested structures
5. **Use interactive mode for exploration**: Great for getting familiar with a new codebase

## Troubleshooting

### Common Issues

1. **Permission denied errors**: The tool will skip files it can't access
2. **Large files**: Files over 100MB are skipped by default
3. **Binary files**: Binary files are detected and excluded from line counting
4. **Encoding issues**: The tool handles UTF-8 encoding errors gracefully

### Performance Tips

1. **Use ignore patterns**: Exclude unnecessary directories like `node_modules`, `venv`, etc.
2. **Limit depth**: Use --max-depth for very large projects
3. **Run on SSD**: Faster disk access improves performance
4. **Close other applications**: Free up system resources for large analyses