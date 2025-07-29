"""
Core analyzer class for the Codebase Analyzer
"""

import os
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable
from datetime import datetime

from .models import (
    AnalysisResult, ProjectStats, FileInfo, AnalysisContext, 
    AnalysisProgress, file_type_registry
)
from .config import Config, get_config
from ..utils.logger import get_logger

logger = get_logger(__name__)


class CodebaseAnalyzer:
    """Main analyzer class for codebase analysis"""
    
    def __init__(
        self, 
        project_path: Union[str, Path],
        config: Optional[Config] = None,
        ignore_patterns: Optional[List[str]] = None,
        max_depth: Optional[int] = None,
        progress_callback: Optional[Callable[[AnalysisProgress], None]] = None
    ):
        self.project_path = Path(project_path).resolve()
        self.config = config or get_config()
        self.ignore_patterns = ignore_patterns or []
        self.max_depth = max_depth or self.config.max_depth
        self.progress_callback = progress_callback
        
        # Analysis context
        self.context = AnalysisContext(
            project_path=self.project_path,
            config=self.config.dict(),
            ignore_patterns=self.ignore_patterns,
            max_depth=self.max_depth,
            follow_symlinks=self.config.follow_symlinks,
            include_hidden=self.config.include_hidden
        )
        
        # Progress tracking
        self.progress = AnalysisProgress()
        
        # Analysis results
        self._result: Optional[AnalysisResult] = None
        
        logger.info(f"Initialized analyzer for project: {self.project_path}")
    
    def analyze(self) -> AnalysisResult:
        """Perform complete analysis of the codebase"""
        start_time = time.time()
        
        logger.info(f"Starting analysis of {self.project_path}")
        
        if not self.project_path.exists():
            raise FileNotFoundError(f"Path does not exist: {self.project_path}")
        
        # Initialize progress tracking
        self.progress.start_time = datetime.now()
        self.progress.total_items = self._count_items()
        
        # Initialize result structure
        stats = ProjectStats()
        files = []
        largest_files = []
        
        # Perform analysis
        try:
            self._analyze_directory(
                self.project_path, 
                stats, 
                files, 
                largest_files, 
                depth=0
            )
            
            # Create analysis result
            analysis_duration = time.time() - start_time
            
            self._result = AnalysisResult(
                project_path=str(self.project_path),
                analysis_date=datetime.now(),
                stats=stats,
                files=files,
                largest_files=largest_files[:10],  # Keep top 10
                analysis_duration=analysis_duration,
                config=self.config.dict()
            )
            
            logger.info(f"Analysis completed in {analysis_duration:.2f} seconds")
            logger.info(f"Found {stats.total_files} files, {stats.total_dirs} directories")
            
            return self._result
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            raise
    
    def _count_items(self) -> int:
        """Count total items to analyze for progress tracking"""
        count = 0
        try:
            for root, dirs, files in os.walk(self.project_path):
                # Check if we should skip this directory
                if self._should_skip_directory(Path(root)):
                    dirs.clear()  # Don't traverse into this directory
                    continue
                
                # Count files in this directory
                for file in files:
                    file_path = Path(root) / file
                    if not self._should_ignore_file(file_path):
                        count += 1
        except Exception as e:
            logger.warning(f"Error counting items: {e}")
        
        return count
    
    def _should_skip_directory(self, directory: Path) -> bool:
        """Check if directory should be skipped"""
        # Check max depth
        if self.max_depth is not None:
            relative_depth = len(directory.relative_to(self.project_path).parts)
            if relative_depth > self.max_depth:
                return True
        
        # Check ignore patterns
        return self.config.should_ignore_file(directory, self.ignore_patterns)
    
    def _should_ignore_file(self, file_path: Path) -> bool:
        """Check if file should be ignored"""
        # Check ignore patterns
        if self.config.should_ignore_file(file_path, self.ignore_patterns):
            return True
        
        # Check file size limit
        try:
            if file_path.stat().st_size > self.config.max_file_size_mb * 1024 * 1024:
                logger.debug(f"Skipping large file: {file_path}")
                return True
        except (OSError, PermissionError):
            logger.debug(f"Cannot access file: {file_path}")
            return True
        
        return False
    
    def _analyze_directory(
        self, 
        directory: Path, 
        stats: ProjectStats, 
        files: List[FileInfo], 
        largest_files: List[FileInfo], 
        depth: int
    ) -> None:
        """Recursively analyze directory structure"""
        if self._should_skip_directory(directory):
            return
        
        try:
            for item in directory.iterdir():
                # Skip hidden files/directories if not included
                if not self.config.include_hidden and item.name.startswith('.'):
                    continue
                
                if item.is_file():
                    if not self._should_ignore_file(item):
                        file_info = self._analyze_file(item)
                        if file_info:
                            files.append(file_info)
                            stats.total_files += 1
                            stats.total_size += file_info.size
                            stats.total_lines += file_info.lines
                            
                            # Update type statistics
                            file_type = file_info.type
                            stats.file_types[file_type] = stats.file_types.get(file_type, 0) + 1
                            stats.file_sizes[file_type] = stats.file_sizes.get(file_type, 0) + file_info.size
                            stats.lines_by_type[file_type] = stats.lines_by_type.get(file_type, 0) + file_info.lines
                            
                            # Track largest files
                            largest_files.append(file_info)
                            largest_files.sort(key=lambda x: x.size, reverse=True)
                            if len(largest_files) > 20:  # Keep only top 20 during analysis
                                largest_files.pop()
                            
                            # Update progress
                            self.progress.processed_items += 1
                            self.progress.current_file = str(item)
                            if self.progress_callback:
                                self.progress_callback(self.progress)
                
                elif item.is_dir():
                    stats.total_dirs += 1
                    if self.max_depth is None or depth < self.max_depth:
                        self._analyze_directory(
                            item, stats, files, largest_files, depth + 1
                        )
        
        except (PermissionError, OSError) as e:
            logger.warning(f"Cannot access directory {directory}: {e}")
    
    def _analyze_file(self, file_path: Path) -> Optional[FileInfo]:
        """Analyze a single file and return metrics"""
        try:
            stat = file_path.stat()
            file_size = stat.st_size
            file_type = file_type_registry.get_file_type(file_path)
            
            # Initialize line counts
            lines = 0
            code_lines = 0
            comment_lines = 0
            blank_lines = 0
            
            # Only analyze text files for line counting
            if self.config.is_text_file(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = self._count_lines(f, file_path)
                        code_lines, comment_lines, blank_lines = self._analyze_line_types(f, file_path)
                except (UnicodeDecodeError, PermissionError, OSError) as e:
                    logger.debug(f"Error reading file {file_path}: {e}")
                    # Binary file or permission denied - set all counts to 0
                    lines = code_lines = comment_lines = blank_lines = 0
            
            return FileInfo(
                path=str(file_path),
                name=file_path.name,
                type=file_type,
                size=file_size,
                lines=lines,
                code_lines=code_lines,
                comment_lines=comment_lines,
                blank_lines=blank_lines,
                extension=file_path.suffix.lower(),
                last_modified=datetime.fromtimestamp(stat.st_mtime)
            )
            
        except (PermissionError, OSError) as e:
            logger.debug(f"Cannot analyze file {file_path}: {e}")
            return None
    
    def _count_lines(self, file_handle, file_path: Path) -> int:
        """Count total lines in a file"""
        file_handle.seek(0)
        return sum(1 for _ in file_handle)
    
    def _analyze_line_types(self, file_handle, file_path: Path) -> tuple[int, int, int]:
        """Analyze line types (code, comments, blank)"""
        file_handle.seek(0)
        
        comment_patterns = self.config.get_comment_patterns_for_file(file_path)
        code_lines = 0
        comment_lines = 0
        blank_lines = 0
        
        in_multiline_comment = False
        
        for line in file_handle:
            stripped = line.strip()
            
            if not stripped:
                blank_lines += 1
                continue
            
            # Check for multi-line comments
            if comment_patterns.multi_start and comment_patterns.multi_start in stripped:
                in_multiline_comment = True
                comment_lines += 1
                continue
            
            if comment_patterns.multi_end and comment_patterns.multi_end in stripped:
                in_multiline_comment = False
                comment_lines += 1
                continue
            
            if in_multiline_comment:
                comment_lines += 1
                continue
            
            # Check for single-line comments
            if comment_patterns.single and stripped.startswith(comment_patterns.single):
                comment_lines += 1
                continue
            
            # Must be code
            code_lines += 1
        
        return code_lines, comment_lines, blank_lines
    
    def get_result(self) -> Optional[AnalysisResult]:
        """Get the analysis result"""
        return self._result
    
    def export_result(self, format_type: str, output_path: Optional[Union[str, Path]] = None) -> None:
        """Export analysis result to various formats"""
        if self._result is None:
            raise RuntimeError("No analysis result available. Run analyze() first.")
        
        from ..exporters.base import exporter_registry
        
        exporter = exporter_registry.get_exporter_for_format(format_type)
        if exporter is None:
            raise ValueError(f"Unsupported export format: {format_type}")
        
        if output_path is None:
            extension = format_type.lower()
            filename = exporter.get_default_filename(self._result, extension)
            output_path = Path(self.config.export_settings.directory) / filename
        
        exporter.export(self._result, output_path)
        logger.info(f"Results exported to: {output_path}")
    
    def generate_report(self, detailed: bool = False) -> str:
        """Generate a formatted report"""
        if self._result is None:
            raise RuntimeError("No analysis result available. Run analyze() first.")
        
        from ..reporters.base import reporter_registry
        
        # Try to use rich reporter if available, otherwise fall back to text
        try:
            reporter = reporter_registry.create('rich')
        except ValueError:
            reporter = reporter_registry.create('text')
        
        return reporter.generate_report(self._result, detailed)
    
    def display_report(self, detailed: bool = False) -> None:
        """Display a formatted report to console"""
        if self._result is None:
            raise RuntimeError("No analysis result available. Run analyze() first.")
        
        from ..reporters.base import reporter_registry
        
        # Try to use rich reporter if available, otherwise fall back to text
        try:
            reporter = reporter_registry.create('rich')
        except ValueError:
            reporter = reporter_registry.create('text')
        
        reporter.display_report(self._result, detailed)