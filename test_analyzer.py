#!/usr/bin/env python3
"""
Test script for the Codebase Analyzer
Demonstrates various features and usage patterns
"""

import os
import tempfile
import shutil
from pathlib import Path
from analyzer import CodebaseAnalyzer, cli
import click.testing

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
    
    # Create JavaScript files
    (project_dir / "web").mkdir()
    (project_dir / "web" / "index.html").write_text("""<!DOCTYPE html>
<html>
<head>
    <title>Sample Web App</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>Welcome to Sample App</h1>
    <div id="app"></div>
    <script src="app.js"></script>
</body>
</html>
""")
    
    (project_dir / "web" / "styles.css").write_text("""/* Sample CSS styles */
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f0f0f0;
}

h1 {
    color: #333;
    text-align: center;
}

#app {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
""")
    
    (project_dir / "web" / "app.js").write_text("""// Sample JavaScript application
class SampleApp {
    constructor() {
        this.data = [];
        this.init();
    }
    
    init() {
        console.log('Initializing app...');
        this.loadData();
        this.render();
    }
    
    loadData() {
        // Simulate loading data
        this.data = [
            { id: 1, name: 'Item 1' },
            { id: 2, name: 'Item 2' },
            { id: 3, name: 'Item 3' }
        ];
    }
    
    render() {
        const app = document.getElementById('app');
        app.innerHTML = this.data.map(item => 
            `<div class="item">${item.name}</div>`
        ).join('');
    }
}

// Initialize the app
new SampleApp();
""")
    
    # Create configuration files
    (project_dir / "config.json").write_text("""{
    "app_name": "Sample Project",
    "version": "1.0.0",
    "debug": true,
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "sample_db"
    }
}
""")
    
    (project_dir / "requirements.txt").write_text("""click>=8.1.0
rich>=13.0.0
pygments>=2.15.0
tabulate>=0.9.0
colorama>=0.4.6
""")
    
    # Create documentation
    (project_dir / "README.md").write_text("""# Sample Project

This is a sample project for testing the codebase analyzer.

## Features

- Python backend
- JavaScript frontend
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

## License

MIT
""")
    
    # Create some binary files (simulated)
    (project_dir / "data.bin").write_bytes(b'\x00\x01\x02\x03\x04\x05')
    
    # Create a large text file
    large_file = project_dir / "large_file.txt"
    with open(large_file, 'w') as f:
        for i in range(1000):
            f.write(f"This is line {i+1} of the large file.\n")
    
    return str(project_dir)

def test_basic_analysis():
    """Test basic analysis functionality"""
    print("🧪 Testing basic analysis...")
    
    project_path = create_sample_project()
    analyzer = CodebaseAnalyzer(project_path)
    stats = analyzer.analyze()
    
    print(f"✅ Analysis completed!")
    print(f"   Files: {stats['total_files']}")
    print(f"   Directories: {stats['total_dirs']}")
    print(f"   Lines: {stats['total_lines']}")
    print(f"   Size: {stats['total_size'] / 1024:.1f} KB")
    print(f"   File types: {len(stats['file_types'])}")
    
    return stats

def test_detailed_analysis():
    """Test detailed analysis with rich output"""
    print("\n🧪 Testing detailed analysis...")
    
    project_path = create_sample_project()
    analyzer = CodebaseAnalyzer(project_path)
    stats = analyzer.analyze()
    
    # Generate detailed report
    report = analyzer.generate_report(detailed=True)
    print("📊 Detailed Report:")
    print(report)
    
    return stats

def test_export_functionality():
    """Test export functionality"""
    print("\n🧪 Testing export functionality...")
    
    project_path = create_sample_project()
    analyzer = CodebaseAnalyzer(project_path)
    stats = analyzer.analyze()
    
    # Test JSON export
    analyzer.export_results('json', 'test_analysis.json')
    
    # Test CSV export
    analyzer.export_results('csv', 'test_analysis.csv')
    
    # Test TXT export
    analyzer.export_results('txt', 'test_analysis.txt')
    
    print("✅ Export tests completed!")
    
    # Clean up
    for file in ['test_analysis.json', 'test_analysis.csv', 'test_analysis.txt']:
        if os.path.exists(file):
            os.remove(file)

def test_cli_commands():
    """Test CLI commands"""
    print("\n🧪 Testing CLI commands...")
    
    project_path = create_sample_project()
    runner = click.testing.CliRunner()
    
    # Test analyze command
    result = runner.invoke(cli, ['analyze', project_path])
    print(f"✅ Analyze command: {'PASS' if result.exit_code == 0 else 'FAIL'}")
    
    # Test stats command
    result = runner.invoke(cli, ['stats', project_path])
    print(f"✅ Stats command: {'PASS' if result.exit_code == 0 else 'FAIL'}")
    
    # Test structure command
    result = runner.invoke(cli, ['structure', project_path])
    print(f"✅ Structure command: {'PASS' if result.exit_code == 0 else 'FAIL'}")

def test_ignore_patterns():
    """Test ignore patterns functionality"""
    print("\n🧪 Testing ignore patterns...")
    
    project_path = create_sample_project()
    
    # Create some files that should be ignored
    project_dir = Path(project_path)
    (project_dir / "__pycache__").mkdir()
    (project_dir / "__pycache__" / "test.pyc").write_bytes(b'\x00\x01\x02')
    (project_dir / ".git").mkdir()
    (project_dir / ".git" / "config").write_text("[core]\nrepositoryformatversion = 0")
    
    # Test with default ignore patterns
    analyzer = CodebaseAnalyzer(project_path)
    stats_default = analyzer.analyze()
    
    # Test with custom ignore patterns
    custom_ignore = ['*.txt', 'web/*']
    analyzer_custom = CodebaseAnalyzer(project_path, custom_ignore)
    stats_custom = analyzer_custom.analyze()
    
    print(f"✅ Default ignore: {stats_default['total_files']} files")
    print(f"✅ Custom ignore: {stats_custom['total_files']} files")
    print(f"   Difference: {stats_default['total_files'] - stats_custom['total_files']} files ignored")

def test_file_type_detection():
    """Test file type detection"""
    print("\n🧪 Testing file type detection...")
    
    project_path = create_sample_project()
    analyzer = CodebaseAnalyzer(project_path)
    stats = analyzer.analyze()
    
    print("📁 File types found:")
    for file_type, count in sorted(stats['file_types'].items(), key=lambda x: x[1], reverse=True):
        lines = stats['lines_by_type'][file_type]
        size_mb = stats['file_sizes'][file_type] / (1024*1024)
        print(f"   {file_type}: {count} files, {lines} lines, {size_mb:.2f} MB")

def run_performance_test():
    """Run a performance test with a larger project"""
    print("\n🧪 Running performance test...")
    
    temp_dir = tempfile.mkdtemp()
    project_dir = Path(temp_dir) / "large_project"
    project_dir.mkdir()
    
    # Create many files
    for i in range(100):
        file_dir = project_dir / f"module_{i}"
        file_dir.mkdir()
        
        for j in range(10):
            py_file = file_dir / f"file_{j}.py"
            py_file.write_text(f"""# Module {i}, File {j}
def function_{j}():
    return {j}

class Class_{j}:
    def __init__(self):
        self.value = {j}
""")
    
    import time
    start_time = time.time()
    
    analyzer = CodebaseAnalyzer(str(project_dir))
    stats = analyzer.analyze()
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"✅ Performance test completed!")
    print(f"   Files processed: {stats['total_files']}")
    print(f"   Time taken: {duration:.2f} seconds")
    print(f"   Files per second: {stats['total_files'] / duration:.1f}")

def main():
    """Run all tests"""
    print("🚀 Starting Codebase Analyzer Tests")
    print("=" * 50)
    
    try:
        # Run all tests
        test_basic_analysis()
        test_detailed_analysis()
        test_export_functionality()
        test_cli_commands()
        test_ignore_patterns()
        test_file_type_detection()
        run_performance_test()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed successfully!")
        print("\n🎉 The Codebase Analyzer is working correctly!")
        print("\nTo use the tool:")
        print("  python analyzer.py analyze /path/to/your/codebase")
        print("  python analyzer.py stats /path/to/your/codebase")
        print("  python analyzer.py structure /path/to/your/codebase")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()