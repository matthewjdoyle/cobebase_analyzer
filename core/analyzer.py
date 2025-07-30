"""
Core codebase analysis functionality
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict

# Rich imports for progress tracking
try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from core.file_analyzer import FileAnalyzer
from utils.file_utils import should_ignore_path, DEFAULT_IGNORE_PATTERNS


class CodebaseAnalyzer:
    """Main analyzer class for codebase analysis"""
    
    def __init__(self, path: str, ignore_patterns: List[str] = None, max_depth: int = None):
        self.path = Path(path).resolve()
        self.ignore_patterns = ignore_patterns or DEFAULT_IGNORE_PATTERNS
        self.max_depth = max_depth
        self.console = Console() if RICH_AVAILABLE else None
        self.file_analyzer = FileAnalyzer()
        
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
                self._analyze_directory(self.path)
        else:
            print("Analyzing codebase...")
            self._analyze_directory(self.path)
        
        return self.stats
    
    def _analyze_directory(self, directory: Path, depth: int = 0) -> None:
        """Recursively analyze directory structure"""
        if self.max_depth and depth > self.max_depth:
            return
            
        if should_ignore_path(directory, self.ignore_patterns):
            return
        
        try:
            for item in directory.iterdir():
                if should_ignore_path(item, self.ignore_patterns):
                    continue
                
                if item.is_file():
                    file_analysis = self.file_analyzer.analyze_file(item)
                    if file_analysis:
                        self._update_stats(file_analysis)
                
                elif item.is_dir():
                    self.stats['total_dirs'] += 1
                    self._analyze_directory(item, depth + 1)
                    
        except (PermissionError, OSError):
            pass
    
    def _update_stats(self, file_analysis: Dict[str, Any]) -> None:
        """Update statistics with file analysis results"""
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