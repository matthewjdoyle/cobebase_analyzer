#!/usr/bin/env python3
"""
Installation script for Codebase Analyzer v2.0
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
            from src.cobebase_analyzer.core.config import create_default_config
            create_default_config(config_file)
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
        from src.cobebase_analyzer.core.analyzer import CodebaseAnalyzer
        from src.cobebase_analyzer.core.config import Config
        from src.cobebase_analyzer.core.models import AnalysisResult
        print("✅ Import test passed")
        
        # Test if the CLI works
        from src.cobebase_analyzer.cli.main import cli
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

def run_comprehensive_test():
    """Run the comprehensive test script"""
    print("🧪 Running comprehensive tests...")
    
    try:
        result = subprocess.run([
            sys.executable, "test_refactored.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Comprehensive tests passed")
            return True
        else:
            print("❌ Comprehensive tests failed")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

def main():
    """Main installation function"""
    print("🚀 Installing Codebase Analyzer v2.0")
    print("=" * 50)
    
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
    
    # Run comprehensive tests
    if not run_comprehensive_test():
        print("⚠️  Comprehensive tests failed, but basic functionality may work...")
    
    print("\n" + "=" * 50)
    print("🎉 Installation completed!")
    print("\n📖 Usage examples:")
    print("  cobebase-analyzer analyze /path/to/your/codebase")
    print("  cobebase-analyzer stats /path/to/your/codebase")
    print("  cobebase-analyzer structure /path/to/your/codebase")
    print("  cobebase-analyzer interactive /path/to/your/codebase")
    print("  cobebase-analyzer config")
    print("  cobebase-analyzer export /path/to/your/codebase --format json")
    print("\n📚 For more information, see README.md")
    print("🔄 For migration help, see MIGRATION.md")

if __name__ == "__main__":
    main()