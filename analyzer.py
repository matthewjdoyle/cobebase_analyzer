#!/usr/bin/env python3
"""
Codebase Analyzer - A comprehensive tool for analyzing codebases
"""

import os
import sys
import json
import csv
import click
import mimetypes
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict, Counter
from datetime import datetime
import re

# Rich imports for beautiful output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.tree import Tree
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Warning: Rich library not available. Install with: pip install rich")

# File type mappings
FILE_EXTENSIONS = {
    # Programming Languages
    '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript', '.jsx': 'React JSX',
    '.tsx': 'React TSX', '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.cs': 'C#',
    '.go': 'Go', '.rs': 'Rust', '.php': 'PHP', '.rb': 'Ruby', '.swift': 'Swift',
    '.kt': 'Kotlin', '.scala': 'Scala', '.r': 'R', '.m': 'Objective-C',
    '.pl': 'Perl', '.lua': 'Lua', '.sh': 'Shell', '.ps1': 'PowerShell',
    '.bat': 'Batch', '.vbs': 'VBScript', '.sql': 'SQL', '.hs': 'Haskell',
    '.ml': 'OCaml', '.f90': 'Fortran', '.asm': 'Assembly', '.s': 'Assembly',
    
    # Web Technologies
    '.html': 'HTML', '.htm': 'HTML', '.css': 'CSS', '.scss': 'SCSS',
    '.sass': 'SASS', '.less': 'LESS', '.xml': 'XML', '.svg': 'SVG',
    
    # Configuration & Data
    '.json': 'JSON', '.yaml': 'YAML', '.yml': 'YAML', '.toml': 'TOML',
    '.ini': 'INI', '.cfg': 'Config', '.conf': 'Config', '.env': 'Environment',
    '.properties': 'Properties', '.lock': 'Lock File', '.log': 'Log',
    
    # Documentation
    '.md': 'Markdown', '.rst': 'reStructuredText', '.txt': 'Text',
    '.pdf': 'PDF', '.doc': 'Word', '.docx': 'Word', '.rtf': 'Rich Text',
    
    # Build & Package
    '.pyc': 'Python Bytecode', '.pyo': 'Python Bytecode', '.so': 'Shared Object',
    '.dll': 'Dynamic Library', '.exe': 'Executable', '.jar': 'Java Archive',
    '.war': 'Web Archive', '.ear': 'Enterprise Archive', '.apk': 'Android Package',
    '.ipa': 'iOS Package', '.deb': 'Debian Package', '.rpm': 'RPM Package',
    '.tar': 'Archive', '.gz': 'Compressed', '.zip': 'Archive', '.7z': 'Archive',
    '.rar': 'Archive', '.bz2': 'Compressed', '.xz': 'Compressed',
    
    # Media
    '.jpg': 'Image', '.jpeg': 'Image', '.png': 'Image', '.gif': 'Image',
    '.bmp': 'Image', '.tiff': 'Image', '.ico': 'Icon', '.mp3': 'Audio',
    '.wav': 'Audio', '.mp4': 'Video', '.avi': 'Video', '.mov': 'Video',
    
    # Version Control
    '.git': 'Git Repository', '.gitignore': 'Git Ignore', '.gitattributes': 'Git Attributes',
    
    # IDE & Editor
    '.vscode': 'VS Code', '.idea': 'IntelliJ IDEA', '.sublime-project': 'Sublime Text',
    '.vim': 'Vim', '.emacs': 'Emacs', '.swp': 'Vim Swap', '.swo': 'Vim Swap',
    
    # Other
    '.bak': 'Backup', '.tmp': 'Temporary', '.cache': 'Cache', '.db': 'Database',
    '.sqlite': 'SQLite Database', '.sqlite3': 'SQLite Database'
}

# Common ignore patterns
DEFAULT_IGNORE_PATTERNS = [
    '__pycache__', '.git', '.svn', '.hg', '.DS_Store', 'Thumbs.db',
    'node_modules', 'venv', 'env', '.venv', '.env', 'dist', 'build',
    '*.pyc', '*.pyo', '*.so', '*.dll', '*.exe', '*.log', '*.tmp',
    '.pytest_cache', '.coverage', '.tox', '.mypy_cache'
]

class CodebaseAnalyzer:
    """Main analyzer class for codebase analysis"""
    
    def __init__(self, path: str, ignore_patterns: List[str] = None, max_depth: int = None):
        self.path = Path(path).resolve()
        self.ignore_patterns = ignore_patterns or DEFAULT_IGNORE_PATTERNS
        self.max_depth = max_depth
        self.console = Console() if RICH_AVAILABLE else None
        
        # Analysis results
        self.stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_lines': 0,
            'total_size': 0,
            'file_types': defaultdict(int),
            'file_sizes': defaultdict(int),
            'lines_by_type': defaultdict(int),
            'largest_files': [],
            'file_details': []
        }
    
    def should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored based on patterns"""
        path_str = str(path)
        for pattern in self.ignore_patterns:
            if pattern.startswith('*'):
                if path_str.endswith(pattern[1:]):
                    return True
            elif pattern in path_str:
                return True
        return False
    
    def get_file_type(self, file_path: Path) -> str:
        """Determine file type based on extension"""
        ext = file_path.suffix.lower()
        return FILE_EXTENSIONS.get(ext, 'Unknown')
    
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single file and return metrics"""
        try:
            stat = file_path.stat()
            file_size = stat.st_size
            file_type = self.get_file_type(file_path)
            
            # Count lines
            lines = 0
            code_lines = 0
            comment_lines = 0
            blank_lines = 0
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        lines += 1
                        stripped = line.strip()
                        
                        if not stripped:
                            blank_lines += 1
                        elif stripped.startswith(('#', '//', '/*', '*', '*/', '<!--', '-->')):
                            comment_lines += 1
                        else:
                            code_lines += 1
            except (UnicodeDecodeError, PermissionError, OSError):
                # Binary file or permission denied
                lines = code_lines = comment_lines = blank_lines = 0
            
            return {
                'path': str(file_path),
                'name': file_path.name,
                'type': file_type,
                'size': file_size,
                'lines': lines,
                'code_lines': code_lines,
                'comment_lines': comment_lines,
                'blank_lines': blank_lines,
                'extension': file_path.suffix.lower()
            }
        except (PermissionError, OSError):
            return None
    
    def analyze_directory(self, directory: Path, depth: int = 0) -> None:
        """Recursively analyze directory structure"""
        if self.max_depth and depth > self.max_depth:
            return
            
        if self.should_ignore(directory):
            return
        
        try:
            for item in directory.iterdir():
                if self.should_ignore(item):
                    continue
                
                if item.is_file():
                    file_analysis = self.analyze_file(item)
                    if file_analysis:
                        self.stats['total_files'] += 1
                        self.stats['total_size'] += file_analysis['size']
                        self.stats['total_lines'] += file_analysis['lines']
                        self.stats['file_types'][file_analysis['type']] += 1
                        self.stats['file_sizes'][file_analysis['type']] += file_analysis['size']
                        self.stats['lines_by_type'][file_analysis['type']] += file_analysis['lines']
                        self.stats['file_details'].append(file_analysis)
                        
                        # Track largest files
                        self.stats['largest_files'].append(file_analysis)
                        self.stats['largest_files'].sort(key=lambda x: x['size'], reverse=True)
                        self.stats['largest_files'] = self.stats['largest_files'][:10]
                
                elif item.is_dir():
                    self.stats['total_dirs'] += 1
                    self.analyze_directory(item, depth + 1)
                    
        except (PermissionError, OSError):
            pass
    
    def analyze(self) -> Dict[str, Any]:
        """Perform complete analysis of the codebase"""
        if not self.path.exists():
            raise FileNotFoundError(f"Path does not exist: {self.path}")
        
        if self.console:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("Analyzing codebase...", total=None)
                self.analyze_directory(self.path)
        else:
            print("Analyzing codebase...")
            self.analyze_directory(self.path)
        
        return self.stats
    
    def generate_report(self, detailed: bool = False) -> str:
        """Generate a formatted report"""
        if not RICH_AVAILABLE:
            return self._generate_text_report(detailed)
        
        # Create a console to render tables
        console = Console()
        
        # Render tables to string
        with console.capture() as capture:
            # Summary table
            summary_table = Table(title="📊 Codebase Analysis Summary", box=box.ROUNDED)
            summary_table.add_column("Metric", style="cyan", no_wrap=True, width=20)
            summary_table.add_column("Value", style="green", width=15)
            
            summary_table.add_row("Total Files", str(self.stats['total_files']))
            summary_table.add_row("Total Directories", str(self.stats['total_dirs']))
            summary_table.add_row("Total Lines of Code", f"{self.stats['total_lines']:,}")
            summary_table.add_row("Total Size", f"{self.stats['total_size'] / (1024*1024):.2f} MB")
            
            console.print(summary_table)
            console.print()
            
            # File types table
            file_types_table = Table(title="📁 File Types Breakdown", box=box.ROUNDED)
            file_types_table.add_column("File Type", style="cyan", width=15)
            file_types_table.add_column("Count", style="green", width=8)
            file_types_table.add_column("Lines", style="yellow", width=12)
            file_types_table.add_column("Size (MB)", style="magenta", width=12)
            
            for file_type, count in sorted(self.stats['file_types'].items(), key=lambda x: x[1], reverse=True):
                lines = self.stats['lines_by_type'][file_type]
                size_mb = self.stats['file_sizes'][file_type] / (1024*1024)
                file_types_table.add_row(file_type, str(count), f"{lines:,}", f"{size_mb:.2f}")
            
            console.print(file_types_table)
            console.print()
            
            # Project tree with file statistics
            tree = self._create_project_tree_with_stats(self.path)
            console.print(Panel.fit("🌳 Project Structure with File Statistics", style="bold blue"))
            console.print(tree)
            
            if detailed:
                console.print()
                # Largest files table
                largest_files_table = Table(title="📏 Largest Files", box=box.ROUNDED)
                largest_files_table.add_column("File", style="cyan", width=25)
                largest_files_table.add_column("Type", style="green", width=12)
                largest_files_table.add_column("Size (KB)", style="yellow", width=12)
                largest_files_table.add_column("Lines", style="magenta", width=8)
                
                for file_info in self.stats['largest_files'][:10]:
                    size_kb = file_info['size'] / 1024
                    largest_files_table.add_row(
                        file_info['name'],
                        file_info['type'],
                        f"{size_kb:.1f}",
                        str(file_info['lines'])
                    )
                
                console.print(largest_files_table)
                console.print()
                
                # Add detailed metrics
                detailed_table = Table(title="🔍 Detailed Metrics", box=box.ROUNDED)
                detailed_table.add_column("File Type", style="cyan", width=15)
                detailed_table.add_column("Code Lines", style="green", width=12)
                detailed_table.add_column("Comment Lines", style="yellow", width=15)
                detailed_table.add_column("Blank Lines", style="magenta", width=12)
                detailed_table.add_column("Comment Ratio", style="blue", width=15)
                
                for file_type in self.stats['file_types']:
                    files_of_type = [f for f in self.stats['file_details'] if f['type'] == file_type]
                    total_code = sum(f['code_lines'] for f in files_of_type)
                    total_comments = sum(f['comment_lines'] for f in files_of_type)
                    total_blank = sum(f['blank_lines'] for f in files_of_type)
                    comment_ratio = (total_comments / (total_code + total_comments)) * 100 if (total_code + total_comments) > 0 else 0
                    
                    detailed_table.add_row(
                        file_type,
                        f"{total_code:,}",
                        f"{total_comments:,}",
                        f"{total_blank:,}",
                        f"{comment_ratio:.1f}%"
                    )
                
                console.print(detailed_table)
        
        return capture.get()
    
    def _display_report(self, detailed: bool = False) -> None:
        """Display report directly to console for cleaner output"""
        if not RICH_AVAILABLE:
            return
        
        console = Console()
        
        # Summary table
        summary_table = Table(title="📊 Codebase Analysis Summary", box=box.ROUNDED)
        summary_table.add_column("Metric", style="cyan", no_wrap=True, width=20)
        summary_table.add_column("Value", style="green", width=15)
        
        summary_table.add_row("Total Files", str(self.stats['total_files']))
        summary_table.add_row("Total Directories", str(self.stats['total_dirs']))
        summary_table.add_row("Total Lines of Code", f"{self.stats['total_lines']:,}")
        summary_table.add_row("Total Size", f"{self.stats['total_size'] / (1024*1024):.2f} MB")
        
        console.print(summary_table)
        console.print()
        
        # File types table
        file_types_table = Table(title="📁 File Types Breakdown", box=box.ROUNDED)
        file_types_table.add_column("File Type", style="cyan", width=15)
        file_types_table.add_column("Count", style="green", width=8)
        file_types_table.add_column("Lines", style="yellow", width=12)
        file_types_table.add_column("Size (MB)", style="magenta", width=12)
        
        for file_type, count in sorted(self.stats['file_types'].items(), key=lambda x: x[1], reverse=True):
            lines = self.stats['lines_by_type'][file_type]
            size_mb = self.stats['file_sizes'][file_type] / (1024*1024)
            file_types_table.add_row(file_type, str(count), f"{lines:,}", f"{size_mb:.2f}")
        
        console.print(file_types_table)
        console.print()
        
        # Project tree with file statistics
        tree = self._create_project_tree_with_stats(self.path)
        console.print(Panel.fit("🌳 Project Structure with File Statistics", style="bold blue"))
        console.print(tree)
        
        if detailed:
            console.print()
            # Largest files table
            largest_files_table = Table(title="📏 Largest Files", box=box.ROUNDED)
            largest_files_table.add_column("File", style="cyan", width=25)
            largest_files_table.add_column("Type", style="green", width=12)
            largest_files_table.add_column("Size (KB)", style="yellow", width=12)
            largest_files_table.add_column("Lines", style="magenta", width=8)
            
            for file_info in self.stats['largest_files'][:10]:
                size_kb = file_info['size'] / 1024
                largest_files_table.add_row(
                    file_info['name'],
                    file_info['type'],
                    f"{size_kb:.1f}",
                    str(file_info['lines'])
                )
            
            console.print(largest_files_table)
            console.print()
            
            # Add detailed metrics
            detailed_table = Table(title="🔍 Detailed Metrics", box=box.ROUNDED)
            detailed_table.add_column("File Type", style="cyan", width=15)
            detailed_table.add_column("Code Lines", style="green", width=12)
            detailed_table.add_column("Comment Lines", style="yellow", width=15)
            detailed_table.add_column("Blank Lines", style="magenta", width=12)
            detailed_table.add_column("Comment Ratio", style="blue", width=15)
            
            for file_type in self.stats['file_types']:
                files_of_type = [f for f in self.stats['file_details'] if f['type'] == file_type]
                total_code = sum(f['code_lines'] for f in files_of_type)
                total_comments = sum(f['comment_lines'] for f in files_of_type)
                total_blank = sum(f['blank_lines'] for f in files_of_type)
                comment_ratio = (total_comments / (total_code + total_comments)) * 100 if (total_code + total_comments) > 0 else 0
                
                detailed_table.add_row(
                    file_type,
                    f"{total_code:,}",
                    f"{total_comments:,}",
                    f"{total_blank:,}",
                    f"{comment_ratio:.1f}%"
                )
            
            console.print(detailed_table)
    
    def _create_project_tree_with_stats(self, path: Path, max_depth: int = 3, current_depth: int = 0):
        """Create a tree visualization with file statistics"""
        if not RICH_AVAILABLE:
            return None
        
        from rich.tree import Tree
        
        # Get file info for this path
        file_info = None
        for file_detail in self.stats['file_details']:
            if Path(file_detail['path']) == path:
                file_info = file_detail
                break
        
        if path.is_file():
            if file_info:
                size_kb = file_info['size'] / 1024
                tree = Tree(f"📄 {path.name} ({file_info['type']}) - {size_kb:.1f}KB, {file_info['lines']} lines")
            else:
                tree = Tree(f"📄 {path.name}")
        else:
            tree = Tree(f"📁 {path.name}")
        
        if current_depth >= max_depth:
            tree.add("...")
            return tree
        
        try:
            items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
            for item in items[:20]:  # Limit to first 20 items
                if self.should_ignore(item):
                    continue
                
                if item.is_file():
                    # Find file info
                    item_info = None
                    for file_detail in self.stats['file_details']:
                        if Path(file_detail['path']) == item:
                            item_info = file_detail
                            break
                    
                    if item_info:
                        size_kb = item_info['size'] / 1024
                        tree.add(f"📄 {item.name} ({item_info['type']}) - {size_kb:.1f}KB, {item_info['lines']} lines")
                    else:
                        tree.add(f"📄 {item.name}")
                
                elif item.is_dir():
                    subtree = self._create_project_tree_with_stats(item, max_depth, current_depth + 1)
                    if subtree:
                        tree.add(subtree)
            
            if len(list(path.iterdir())) > 20:
                tree.add("...")
        except (PermissionError, OSError):
            tree.add("❌ Access denied")
        
        return tree
    
    def _generate_text_report(self, detailed: bool = False) -> str:
        """Generate plain text report when rich is not available"""
        report = []
        report.append("=" * 60)
        report.append("CODEBASE ANALYSIS SUMMARY")
        report.append("=" * 60)
        report.append(f"Total Files: {self.stats['total_files']}")
        report.append(f"Total Directories: {self.stats['total_dirs']}")
        report.append(f"Total Lines of Code: {self.stats['total_lines']:,}")
        report.append(f"Total Size: {self.stats['total_size'] / (1024*1024):.2f} MB")
        report.append("")
        
        report.append("FILE TYPES BREAKDOWN:")
        report.append("-" * 30)
        for file_type, count in sorted(self.stats['file_types'].items(), key=lambda x: x[1], reverse=True):
            lines = self.stats['lines_by_type'][file_type]
            size_mb = self.stats['file_sizes'][file_type] / (1024*1024)
            report.append(f"{file_type}: {count} files, {lines:,} lines, {size_mb:.2f} MB")
        
        report.append("")
        report.append("PROJECT STRUCTURE WITH FILE STATISTICS:")
        report.append("-" * 45)
        report.extend(self._generate_text_tree_with_stats(self.path))
        
        if detailed:
            report.append("")
            report.append("LARGEST FILES:")
            report.append("-" * 20)
            for file_info in self.stats['largest_files'][:10]:
                size_kb = file_info['size'] / 1024
                report.append(f"{file_info['name']} ({file_info['type']}): {size_kb:.1f} KB, {file_info['lines']} lines")
            
            report.append("")
            report.append("DETAILED METRICS:")
            report.append("-" * 20)
            for file_type in self.stats['file_types']:
                files_of_type = [f for f in self.stats['file_details'] if f['type'] == file_type]
                total_code = sum(f['code_lines'] for f in files_of_type)
                total_comments = sum(f['comment_lines'] for f in files_of_type)
                total_blank = sum(f['blank_lines'] for f in files_of_type)
                comment_ratio = (total_comments / (total_code + total_comments)) * 100 if (total_code + total_comments) > 0 else 0
                report.append(f"{file_type}: {total_code:,} code, {total_comments:,} comments, {total_blank:,} blank ({comment_ratio:.1f}% comments)")
        
        return "\n".join(report)
    
    def _generate_text_tree_with_stats(self, path: Path, prefix: str = "", max_depth: int = 3, current_depth: int = 0) -> List[str]:
        """Generate text-based tree with file statistics"""
        lines = []
        
        if current_depth >= max_depth:
            lines.append(f"{prefix}...")
            return lines
        
        try:
            items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
            for i, item in enumerate(items[:20]):  # Limit to first 20 items
                if self.should_ignore(item):
                    continue
                
                is_last = (i == len(items) - 1) or (i == 19 and len(items) > 20)
                current_prefix = prefix + ("└── " if is_last else "├── ")
                
                if item.is_file():
                    # Find file info
                    item_info = None
                    for file_detail in self.stats['file_details']:
                        if Path(file_detail['path']) == item:
                            item_info = file_detail
                            break
                    
                    if item_info:
                        size_kb = item_info['size'] / 1024
                        lines.append(f"{current_prefix}{item.name} ({item_info['type']}) - {size_kb:.1f}KB, {item_info['lines']} lines")
                    else:
                        lines.append(f"{current_prefix}{item.name}")
                
                elif item.is_dir():
                    lines.append(f"{current_prefix}{item.name}/")
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    lines.extend(self._generate_text_tree_with_stats(item, next_prefix, max_depth, current_depth + 1))
            
            if len(items) > 20:
                lines.append(f"{prefix}...")
                
        except (PermissionError, OSError):
            lines.append(f"{prefix}❌ Access denied")
        
        return lines
    
    def export_results(self, format_type: str, output_file: str = None) -> None:
        """Export analysis results to various formats"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"codebase_analysis_{timestamp}.{format_type}"
        
        if format_type.lower() == 'json':
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, default=str)
        
        elif format_type.lower() == 'csv':
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['File Type', 'Count', 'Lines', 'Size (bytes)'])
                for file_type, count in self.stats['file_types'].items():
                    lines = self.stats['lines_by_type'][file_type]
                    size = self.stats['file_sizes'][file_type]
                    writer.writerow([file_type, count, lines, size])
        
        elif format_type.lower() == 'txt':
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(self._generate_text_report(detailed=True))
        
        if self.console:
            self.console.print(f"✅ Results exported to: {output_file}", style="green")
        else:
            print(f"Results exported to: {output_file}")

def create_project_tree(path: Path, max_depth: int = 3, current_depth: int = 0):
    """Create a tree visualization of the project structure"""
    if not RICH_AVAILABLE:
        return None
    
    from rich.tree import Tree
    
    tree = Tree(f"📁 {path.name}")
    
    if current_depth >= max_depth:
        tree.add("...")
        return tree
    
    try:
        items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        for item in items[:20]:  # Limit to first 20 items
            if item.is_file():
                tree.add(f"📄 {item.name}")
            elif item.is_dir():
                subtree = create_project_tree(item, max_depth, current_depth + 1)
                if subtree:
                    tree.add(subtree)
        
        if len(list(path.iterdir())) > 20:
            tree.add("...")
    except (PermissionError, OSError):
        tree.add("❌ Access denied")
    
    return tree

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Codebase Analyzer - Comprehensive codebase analysis tool"""
    pass

@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--detailed', is_flag=True, help='Include detailed metrics')
@click.option('--export', type=click.Choice(['json', 'csv', 'txt']), help='Export results to file')
@click.option('--ignore', multiple=True, help='Ignore patterns (can be used multiple times)')
@click.option('--max-depth', type=int, help='Maximum directory depth to analyze')
@click.option('--sort-by', type=click.Choice(['size', 'lines', 'name']), default='size', help='Sort results by field')
def analyze(path, detailed, export, ignore, max_depth, sort_by):
    """Analyze a codebase and display comprehensive metrics"""
    try:
        ignore_patterns = list(ignore) if ignore else DEFAULT_IGNORE_PATTERNS
        analyzer = CodebaseAnalyzer(path, ignore_patterns, max_depth)
        
        console = Console() if RICH_AVAILABLE else None
        if console:
            console.print(Panel.fit("🔍 Starting Codebase Analysis", style="bold blue"))
        
        stats = analyzer.analyze()
        
        # Generate and display report
        if console:
            # Display tables directly instead of capturing to string
            analyzer._display_report(detailed)
        else:
            report = analyzer.generate_report(detailed)
            print(report)
        
        if export:
            analyzer.export_results(export)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--max-depth', type=int, default=3, help='Maximum depth to show')
def structure(path, max_depth):
    """Show project structure as a tree"""
    if not RICH_AVAILABLE:
        click.echo("Rich library is required for tree visualization. Install with: pip install rich")
        return
    
    try:
        project_path = Path(path)
        tree = create_project_tree(project_path, max_depth)
        console = Console()
        console.print(tree)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('path', type=click.Path(exists=True))
def stats(path):
    """Quick statistics overview"""
    try:
        analyzer = CodebaseAnalyzer(path)
        stats = analyzer.analyze()
        
        console = Console() if RICH_AVAILABLE else None
        if console:
            summary_table = Table(title="📊 Quick Stats", box=box.ROUNDED)
            summary_table.add_column("Metric", style="cyan", width=15)
            summary_table.add_column("Value", style="green", width=15)
            
            summary_table.add_row("Files", str(stats['total_files']))
            summary_table.add_row("Directories", str(stats['total_dirs']))
            summary_table.add_row("Lines of Code", f"{stats['total_lines']:,}")
            summary_table.add_row("Size", f"{stats['total_size'] / (1024*1024):.2f} MB")
            summary_table.add_row("File Types", str(len(stats['file_types'])))
            
            console.print(summary_table)
        else:
            print(f"Files: {stats['total_files']}")
            print(f"Directories: {stats['total_dirs']}")
            print(f"Lines of Code: {stats['total_lines']:,}")
            print(f"Size: {stats['total_size'] / (1024*1024):.2f} MB")
            print(f"File Types: {len(stats['file_types'])}")
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('path', type=click.Path(exists=True))
def interactive(path):
    """Start interactive exploration mode"""
    if not RICH_AVAILABLE:
        click.echo("Rich library is required for interactive mode. Install with: pip install rich")
        return
    
    console = Console()
    console.print(Panel.fit("🎮 Interactive Codebase Explorer", style="bold green"))
    console.print("Use the following commands:")
    console.print("  tree - Show project structure")
    console.print("  stats - Show quick statistics")
    console.print("  analyze - Full analysis")
    console.print("  quit - Exit")
    
    analyzer = CodebaseAnalyzer(path)
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == 'quit' or command == 'exit':
                break
            elif command == 'tree':
                tree = create_project_tree(Path(path))
                console.print(tree)
            elif command == 'stats':
                stats = analyzer.analyze()
                summary_table = Table(title="📊 Quick Stats", box=box.ROUNDED)
                summary_table.add_column("Metric", style="cyan")
                summary_table.add_column("Value", style="green")
                
                summary_table.add_row("Files", str(stats['total_files']))
                summary_table.add_row("Directories", str(stats['total_dirs']))
                summary_table.add_row("Lines of Code", f"{stats['total_lines']:,}")
                summary_table.add_row("Size", f"{stats['total_size'] / (1024*1024):.2f} MB")
                
                console.print(summary_table)
            elif command == 'analyze':
                stats = analyzer.analyze()
                console.print(analyzer.generate_report(detailed=True))
            else:
                console.print("Unknown command. Type 'quit' to exit.")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"Error: {e}", style="red")

def main():
    """Main entry point"""
    cli()

if __name__ == '__main__':
    main()