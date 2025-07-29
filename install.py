#!/usr/bin/env python3
"""
Installation script for Codebase Analyzer
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def install_package():
    """Install the package in development mode"""
    print("🔧 Installing package...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-e", "."
        ])
        print("✅ Package installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install package: {e}")
        return False

def create_config_file():
    """Create a default configuration file if it doesn't exist"""
    config_file = Path.home() / ".cobebase_analyzer.json"
    
    if not config_file.exists():
        print("⚙️  Creating default configuration file...")
        try:
            import json
            default_config = {
                "max_file_size_mb": 100,
                "max_depth": None,
                "follow_symlinks": False,
                "include_hidden": False,
                "show_progress": True,
                "color_output": True,
                "detailed_by_default": False,
                "ignore_patterns": [
                    "__pycache__", ".git", ".svn", ".hg", ".DS_Store", "Thumbs.db",
                    "node_modules", "venv", "env", ".venv", ".env", "dist", "build",
                    "*.pyc", "*.pyo", "*.so", "*.dll", "*.exe", "*.log", "*.tmp",
                    ".pytest_cache", ".coverage", ".tox", ".mypy_cache"
                ]
            }
            
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            print(f"✅ Configuration file created: {config_file}")
            return True
        except Exception as e:
            print(f"❌ Failed to create configuration file: {e}")
            return False
    else:
        print(f"✅ Configuration file already exists: {config_file}")
        return True

def test_installation():
    """Test if the installation was successful"""
    print("🧪 Testing installation...")
    
    try:
        # Test if we can import the analyzer
        from analyzer import CodebaseAnalyzer, cli
        print("✅ Import test passed")
        
        # Test if the CLI works
        import click.testing
        runner = click.testing.CliRunner()
        result = runner.invoke(cli, ['--help'])
        
        if result.exit_code == 0:
            print("✅ CLI test passed")
            return True
        else:
            print("❌ CLI test failed")
            return False
            
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False

def main():
    """Main installation function"""
    print("🚀 Installing Codebase Analyzer")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Install package
    if not install_package():
        sys.exit(1)
    
    # Create configuration file
    if not create_config_file():
        print("⚠️  Configuration file creation failed, but installation continues...")
    
    # Test installation
    if not test_installation():
        print("⚠️  Installation test failed, but installation may still work...")
    
    print("\n" + "=" * 40)
    print("🎉 Installation completed!")
    print("\n📖 Usage examples:")
    print("  cobebase-analyzer analyze /path/to/your/codebase")
    print("  cobebase-analyzer stats /path/to/your/codebase")
    print("  cobebase-analyzer structure /path/to/your/codebase")
    print("  cobebase-analyzer interactive /path/to/your/codebase")
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()