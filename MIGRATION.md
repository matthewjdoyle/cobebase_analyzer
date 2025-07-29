# Migration Guide: v1.0 to v2.0

This guide helps you migrate from Codebase Analyzer v1.0 to v2.0.

## 🚨 Breaking Changes

### Package Structure

**v1.0:**
```
cobebase_analyzer/
├── analyzer.py
├── config.py
├── setup.py
└── ...
```

**v2.0:**
```
cobebase_analyzer/
├── src/
│   └── cobebase_analyzer/
│       ├── core/
│       ├── reporters/
│       ├── exporters/
│       ├── cli/
│       └── utils/
├── setup.py
└── ...
```

### Import Changes

**v1.0:**
```python
from analyzer import CodebaseAnalyzer
```

**v2.0:**
```python
from cobebase_analyzer.core.analyzer import CodebaseAnalyzer
# or
from cobebase_analyzer import CodebaseAnalyzer
```

### CLI Commands

**v1.0:**
```bash
python analyzer.py analyze /path/to/project
python analyzer.py stats /path/to/project
```

**v2.0:**
```bash
cobebase-analyzer analyze /path/to/project
cobebase-analyzer stats /path/to/project
# or
python -m cobebase_analyzer.cli.main analyze /path/to/project
```

### Configuration Format

**v1.0:** Simple dictionary-based configuration

**v2.0:** Pydantic-based configuration with validation

```python
# v1.0
config = {
    'max_file_size_mb': 100,
    'ignore_patterns': ['*.pyc']
}

# v2.0
from cobebase_analyzer.core.config import Config
config = Config(
    max_file_size_mb=100,
    default_ignore_patterns=['*.pyc']
)
```

## 🔄 Migration Steps

### 1. Update Installation

**Uninstall v1.0:**
```bash
pip uninstall cobebase-analyzer
```

**Install v2.0:**
```bash
git clone https://github.com/matthewjdoyle/codebase_analyzer
cd cobebase_analyzer
pip install -e .
```

### 2. Update Import Statements

**Before (v1.0):**
```python
from analyzer import CodebaseAnalyzer
import config
```

**After (v2.0):**
```python
from cobebase_analyzer import CodebaseAnalyzer, Config
# or
from cobebase_analyzer.core.analyzer import CodebaseAnalyzer
from cobebase_analyzer.core.config import Config
```

### 3. Update Configuration Usage

**Before (v1.0):**
```python
from config import DEFAULT_CONFIG
analyzer = CodebaseAnalyzer(path, ignore_patterns=['*.pyc'])
```

**After (v2.0):**
```python
from cobebase_analyzer.core.config import Config, load_config

# Option 1: Use default config
config = Config()
analyzer = CodebaseAnalyzer(path, config=config, ignore_patterns=['*.pyc'])

# Option 2: Load from file
config = load_config('my_config.json')
analyzer = CodebaseAnalyzer(path, config=config)
```

### 4. Update CLI Usage

**Before (v1.0):**
```bash
python analyzer.py analyze /path/to/project --detailed
python analyzer.py export /path/to/project --format json
```

**After (v2.0):**
```bash
cobebase-analyzer analyze /path/to/project --detailed
cobebase-analyzer export /path/to/project --format json
```

### 5. Update Scripts

**Before (v1.0):**
```python
#!/usr/bin/env python3
from analyzer import CodebaseAnalyzer

analyzer = CodebaseAnalyzer('/path/to/project')
result = analyzer.analyze()
print(f"Found {result['total_files']} files")
```

**After (v2.0):**
```python
#!/usr/bin/env python3
from cobebase_analyzer import CodebaseAnalyzer

analyzer = CodebaseAnalyzer('/path/to/project')
result = analyzer.analyze()
print(f"Found {result.stats.total_files} files")
```

## 🆕 New Features

### 1. Enhanced Configuration

```python
from cobebase_analyzer.core.config import Config

config = Config(
    max_file_size_mb=200,
    max_depth=5,
    follow_symlinks=True,
    complexity_metrics=ComplexityMetrics(
        enabled=True,
        max_function_length=100
    )
)
```

### 2. Multiple Export Formats

```python
# Export to JSON
analyzer.export_result('json', 'analysis.json')

# Export to CSV (creates multiple files)
analyzer.export_result('csv', 'analysis.csv')

# Export to text
analyzer.export_result('txt', 'analysis.txt')
```

### 3. Progress Tracking

```python
def progress_callback(progress):
    print(f"Processed {progress.processed_items}/{progress.total_items} files")

analyzer = CodebaseAnalyzer(
    path, 
    progress_callback=progress_callback
)
```

### 4. Custom Reporters

```python
from cobebase_analyzer.reporters.base import BaseReporter

class CustomReporter(BaseReporter):
    def generate_report(self, result, detailed=False):
        return f"Custom report for {result.stats.total_files} files"

# Register and use
from cobebase_analyzer.reporters.base import reporter_registry
reporter_registry.register('custom', CustomReporter)
```

### 5. Type Safety

```python
from cobebase_analyzer.core.models import AnalysisResult, FileInfo

def process_result(result: AnalysisResult) -> None:
    for file_info in result.files:
        print(f"{file_info.name}: {file_info.lines} lines")
```

## 🐛 Common Issues

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'analyzer'`

**Solution:** Update imports to use the new package structure:
```python
# Old
from analyzer import CodebaseAnalyzer

# New
from cobebase_analyzer import CodebaseAnalyzer
```

### Configuration Errors

**Error:** `TypeError: 'dict' object is not callable`

**Solution:** Use the new Config class:
```python
# Old
config = {'max_file_size_mb': 100}

# New
from cobebase_analyzer.core.config import Config
config = Config(max_file_size_mb=100)
```

### CLI Command Not Found

**Error:** `command not found: cobebase-analyzer`

**Solution:** Install the package properly:
```bash
pip install -e .
# or
python -m pip install -e .
```

### Result Access Errors

**Error:** `TypeError: 'dict' object has no attribute 'stats'`

**Solution:** Use the new result object structure:
```python
# Old
result = analyzer.analyze()
print(result['total_files'])

# New
result = analyzer.analyze()
print(result.stats.total_files)
```

## 📋 Migration Checklist

- [ ] Uninstall v1.0 version
- [ ] Install v2.0 version
- [ ] Update import statements
- [ ] Update configuration usage
- [ ] Update CLI commands
- [ ] Update scripts and automation
- [ ] Test functionality
- [ ] Update documentation

## 🆘 Getting Help

If you encounter issues during migration:

1. Check the [GitHub Issues](https://github.com/matthewjdoyle/codebase_analyzer/issues)
2. Review the [README.md](README.md) for updated usage
3. Run the test script: `python test_refactored.py`
4. Create a new issue with details about your problem

## 🔄 Rollback

If you need to rollback to v1.0:

```bash
pip uninstall cobebase-analyzer
git checkout v1.0
pip install -e .
```

**Note:** Rolling back will require reverting any code changes you made for v2.0 compatibility.