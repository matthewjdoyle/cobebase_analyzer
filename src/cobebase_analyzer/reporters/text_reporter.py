"""
Text reporter implementation for plain text output
"""

from typing import Optional, Dict, Any, List
from pathlib import Path

from .base import BaseReporter
from ..core.models import AnalysisResult

# Register this reporter
from .base import reporter_registry


class TextReporter(BaseReporter):
    """Text-based reporter for plain text output"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
    
    def generate_report(self, result: AnalysisResult, detailed: bool = False) -> str:
        """Generate a plain text report"""
        lines = []
        
        # Header
        lines.append("=" * 60)
        lines.append("CODEBASE ANALYSIS SUMMARY")
        lines.append("=" * 60)
        lines.append(f"Project: {result.project_path}")
        lines.append(f"Analysis Date: {result.analysis_date.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Analysis Duration: {result.analysis_duration:.2f} seconds")
        lines.append("")
        
        # Summary statistics
        summary_stats = self.get_summary_stats(result)
        lines.append("SUMMARY STATISTICS:")
        lines.append("-" * 20)
        lines.append(f"Total Files: {summary_stats['total_files']}")
        lines.append(f"Total Directories: {summary_stats['total_dirs']}")
        lines.append(f"Total Lines of Code: {self.format_number(summary_stats['total_lines'])}")
        lines.append(f"Total Size: {summary_stats['total_size_mb']:.2f} MB")
        lines.append(f"Unique File Types: {summary_stats['unique_file_types']}")
        lines.append(f"Average File Size: {self.format_file_size(int(summary_stats['average_file_size']))}")
        lines.append(f"Average Lines per File: {summary_stats['average_lines_per_file']:.1f}")
        lines.append("")
        
        # File types breakdown
        breakdown = self.get_file_type_breakdown(result)
        lines.append("FILE TYPES BREAKDOWN:")
        lines.append("-" * 30)
        
        # Sort by count descending
        sorted_types = sorted(breakdown.items(), key=lambda x: x[1]['count'], reverse=True)
        
        for file_type, data in sorted_types:
            lines.append(
                f"{file_type}: {data['count']} files, "
                f"{self.format_number(data['lines'])} lines, "
                f"{data['size_mb']:.2f} MB ({data['percentage']:.1f}%)"
            )
        lines.append("")
        
        # Project structure
        lines.append("PROJECT STRUCTURE:")
        lines.append("-" * 20)
        lines.extend(self._generate_project_tree_text(result))
        lines.append("")
        
        if detailed:
            # Largest files
            largest_files = self.get_largest_files(result, 10)
            lines.append("LARGEST FILES:")
            lines.append("-" * 20)
            for file_info in largest_files:
                lines.append(
                    f"{file_info.name} ({file_info.type}): "
                    f"{self.format_file_size(file_info.size)}, "
                    f"{file_info.lines} lines "
                    f"[{file_info.code_lines}/{file_info.comment_lines}/{file_info.blank_lines}]"
                )
            lines.append("")
            
            # Detailed metrics
            detailed_metrics = self.get_detailed_metrics(result)
            lines.append("DETAILED METRICS:")
            lines.append("-" * 20)
            
            # Sort by code lines descending
            sorted_metrics = sorted(detailed_metrics.items(), key=lambda x: x[1]['code_lines'], reverse=True)
            
            for file_type, metrics in sorted_metrics:
                lines.append(
                    f"{file_type}: "
                    f"{self.format_number(metrics['code_lines'])} code, "
                    f"{self.format_number(metrics['comment_lines'])} comments, "
                    f"{self.format_number(metrics['blank_lines'])} blank "
                    f"({metrics['comment_ratio']:.1f}% comments, "
                    f"{metrics['file_count']} files)"
                )
            lines.append("")
        
        return "\n".join(lines)
    
    def display_report(self, result: AnalysisResult, detailed: bool = False) -> None:
        """Display a plain text report to console"""
        report = self.generate_report(result, detailed)
        print(report)
    
    def _generate_project_tree_text(self, result: AnalysisResult, max_depth: int = 3) -> List[str]:
        """Generate text-based project tree"""
        lines = []
        project_path = Path(result.project_path)
        
        def add_tree_node(path: Path, prefix: str = "", current_depth: int = 0) -> None:
            if current_depth >= max_depth:
                lines.append(f"{prefix}...")
                return
            
            try:
                items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
                for i, item in enumerate(items[:20]):  # Limit to first 20 items
                    if self._should_ignore_item(item, result):
                        continue
                    
                    is_last = (i == len(items) - 1) or (i == 19 and len(items) > 20)
                    current_prefix = prefix + ("└── " if is_last else "├── ")
                    
                    if item.is_file():
                        # Find file info
                        item_info = None
                        for file_detail in result.files:
                            if Path(file_detail.path) == item:
                                item_info = file_detail
                                break
                        
                        if item_info:
                            size_str = self.format_file_size(item_info.size)
                            lines.append(
                                f"{current_prefix}{item.name} ({item_info.type}) - "
                                f"{size_str}, {item_info.lines} lines"
                            )
                        else:
                            lines.append(f"{current_prefix}{item.name}")
                    
                    elif item.is_dir():
                        lines.append(f"{current_prefix}{item.name}/")
                        next_prefix = prefix + ("    " if is_last else "│   ")
                        add_tree_node(item, next_prefix, current_depth + 1)
                
                if len(items) > 20:
                    lines.append(f"{prefix}...")
                    
            except (PermissionError, OSError):
                lines.append(f"{prefix}❌ Access denied")
        
        add_tree_node(project_path)
        return lines
    
    def _should_ignore_item(self, item: Path, result: AnalysisResult) -> bool:
        """Check if item should be ignored in tree display"""
        # Check if it's in the analysis results
        if item.is_file():
            return not any(Path(f.path) == item for f in result.files)
        return False


# Register the text reporter
reporter_registry.register('text', TextReporter)