#!/usr/bin/env python3
"""
Test script for the refactored Codebase Analyzer
"""

import os
import tempfile
import shutil
from pathlib import Path

def create_sample_project():
    """Create a sample project structure for testing"""
    temp_dir = tempfile.mkdtemp()
    project_dir = Path(temp_dir) / "sample_project"
    project_dir.mkdir()
    
    # Create Python files
    (project_dir / "src").mkdir()
    (project_dir / "src" / "__init__.py").write_text("# Sample package\n")
    
    main_py = project_dir / "src" / "main.py"
    main_py.write_text("""#!/usr/bin/env python3
\"\"\"
Main application module
This is a sample Python application
\"\"\"

import os
import sys
from typing import List, Dict

class SampleClass:
    \"\"\"A sample class for demonstration\"\"\"
    
    def __init__(self, name: str):
        self.name = name
        self.data = []
    
    def add_item(self, item: str) -> None:
        \"\"\"Add an item to the data list\"\"\"
        self.data.append(item)
    
    def get_items(self) -> List[str]:
        \"\"\"Get all items from the data list\"\"\"
        return self.data.copy()

def main():
    \"\"\"Main function\"\"\"
    print("Hello, World!")
    sample = SampleClass("test")
    sample.add_item("item1")
    sample.add_item("item2")
    print(f"Items: {sample.get_items()}")

if __name__ == "__main__":
    main()
""")
    
    # Create configuration files
    (project_dir / "config.json").write_text("""{
    "app_name": "Sample Project",
    "version": "1.0.0",
    "debug": true
}
""")
    
    # Create documentation
    (project_dir / "README.md").write_text("""# Sample Project

This is a sample project for testing the refactored codebase analyzer.

## Features

- Python backend
- Configuration management
- Documentation

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python src/main.py
```
""")
    
    return str(project_dir)

def test_basic_functionality():
    """Test basic functionality of the refactored analyzer"""
    print("🧪 Testing refactored Codebase Analyzer...")
    
    try:
        # Import the refactored modules
        from src.cobebase_analyzer.core.analyzer import CodebaseAnalyzer
        from src.cobebase_analyzer.core.config import Config
        from src.cobebase_analyzer.core.models import AnalysisResult
        
        print("✅ Imports successful")
        
        # Create sample project
        project_path = create_sample_project()
        print(f"✅ Sample project created at: {project_path}")
        
        # Create analyzer
        analyzer = CodebaseAnalyzer(project_path)
        print("✅ Analyzer created")
        
        # Perform analysis
        result = analyzer.analyze()
        print("✅ Analysis completed")
        
        # Check results
        print(f"   Files: {result.stats.total_files}")
        print(f"   Directories: {result.stats.total_dirs}")
        print(f"   Lines: {result.stats.total_lines}")
        print(f"   Size: {result.stats.total_size_mb:.2f} MB")
        print(f"   File types: {result.stats.unique_file_types}")
        
        # Test report generation
        report = analyzer.generate_report(detailed=False)
        print("✅ Report generation successful")
        
        # Test export
        analyzer.export_result('json', 'test_analysis.json')
        print("✅ JSON export successful")
        
        # Clean up
        if os.path.exists('test_analysis.json'):
            os.remove('test_analysis.json')
        
        print("\n🎉 All tests passed! The refactored project is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_functionality():
    """Test CLI functionality"""
    print("\n🧪 Testing CLI functionality...")
    
    try:
        from src.cobebase_analyzer.cli.main import cli
        import click.testing
        
        print("✅ CLI imports successful")
        
        # Create sample project
        project_path = create_sample_project()
        
        # Test CLI commands
        runner = click.testing.CliRunner()
        
        # Test help
        result = runner.invoke(cli, ['--help'])
        if result.exit_code == 0:
            print("✅ CLI help command works")
        else:
            print("❌ CLI help command failed")
            return False
        
        # Test analyze command
        result = runner.invoke(cli, ['analyze', project_path])
        if result.exit_code == 0:
            print("✅ CLI analyze command works")
        else:
            print("❌ CLI analyze command failed")
            return False
        
        # Test stats command
        result = runner.invoke(cli, ['stats', project_path])
        if result.exit_code == 0:
            print("✅ CLI stats command works")
        else:
            print("❌ CLI stats command failed")
            return False
        
        print("🎉 CLI tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ CLI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Refactored Codebase Analyzer v2.0")
    print("=" * 50)
    
    # Test basic functionality
    basic_success = test_basic_functionality()
    
    # Test CLI functionality
    cli_success = test_cli_functionality()
    
    print("\n" + "=" * 50)
    if basic_success and cli_success:
        print("✅ All tests passed! The refactored project is ready for use.")
        print("\nTo use the tool:")
        print("  python -m src.cobebase_analyzer.cli.main analyze /path/to/your/codebase")
        print("  python -m src.cobebase_analyzer.cli.main stats /path/to/your/codebase")
        print("  python -m src.cobebase_analyzer.cli.main structure /path/to/your/codebase")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())