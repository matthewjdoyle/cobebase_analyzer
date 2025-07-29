"""
Base reporter interface for the Codebase Analyzer
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from ..core.models import AnalysisResult


class BaseReporter(ABC):
    """Base class for all reporters"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
    
    @abstractmethod
    def generate_report(self, result: AnalysisResult, detailed: bool = False) -> str:
        """Generate a report from analysis results"""
        pass
    
    @abstractmethod
    def display_report(self, result: AnalysisResult, detailed: bool = False) -> None:
        """Display a report to the console"""
        pass
    
    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    
    def format_number(self, number: int) -> str:
        """Format large numbers with commas"""
        return f"{number:,}"
    
    def get_summary_stats(self, result: AnalysisResult) -> Dict[str, Any]:
        """Extract summary statistics from analysis result"""
        stats = result.stats
        return {
            'total_files': stats.total_files,
            'total_dirs': stats.total_dirs,
            'total_lines': stats.total_lines,
            'total_size': stats.total_size,
            'total_size_mb': stats.total_size_mb,
            'unique_file_types': stats.unique_file_types,
            'average_file_size': stats.average_file_size,
            'average_lines_per_file': stats.average_lines_per_file
        }
    
    def get_file_type_breakdown(self, result: AnalysisResult) -> Dict[str, Dict[str, Any]]:
        """Get detailed breakdown by file type"""
        breakdown = {}
        stats = result.stats
        
        for file_type, count in stats.file_types.items():
            lines = stats.lines_by_type.get(file_type, 0)
            size = stats.file_sizes.get(file_type, 0)
            
            breakdown[file_type] = {
                'count': count,
                'lines': lines,
                'size': size,
                'size_mb': size / (1024 * 1024),
                'percentage': (count / stats.total_files * 100) if stats.total_files > 0 else 0
            }
        
        return breakdown
    
    def get_largest_files(self, result: AnalysisResult, limit: int = 10) -> list:
        """Get the largest files"""
        return result.get_largest_files(limit)
    
    def get_most_complex_files(self, result: AnalysisResult, limit: int = 10) -> list:
        """Get files with the most lines"""
        return result.get_most_complex_files(limit)
    
    def get_detailed_metrics(self, result: AnalysisResult) -> Dict[str, Dict[str, Any]]:
        """Get detailed metrics by file type"""
        detailed = {}
        
        for file_type in result.stats.file_types:
            files_of_type = result.get_files_by_type(file_type)
            if not files_of_type:
                continue
            
            total_code = sum(f.code_lines for f in files_of_type)
            total_comments = sum(f.comment_lines for f in files_of_type)
            total_blank = sum(f.blank_lines for f in files_of_type)
            total_lines = sum(f.lines for f in files_of_type)
            
            comment_ratio = (total_comments / (total_code + total_comments) * 100) if (total_code + total_comments) > 0 else 0
            
            detailed[file_type] = {
                'code_lines': total_code,
                'comment_lines': total_comments,
                'blank_lines': total_blank,
                'total_lines': total_lines,
                'comment_ratio': comment_ratio,
                'file_count': len(files_of_type)
            }
        
        return detailed


class ReporterRegistry:
    """Registry for managing different reporter types"""
    
    def __init__(self):
        self._reporters: Dict[str, type] = {}
    
    def register(self, name: str, reporter_class: type) -> None:
        """Register a new reporter"""
        if not issubclass(reporter_class, BaseReporter):
            raise ValueError(f"Reporter class must inherit from BaseReporter")
        self._reporters[name] = reporter_class
    
    def get(self, name: str) -> Optional[type]:
        """Get a reporter by name"""
        return self._reporters.get(name)
    
    def list_available(self) -> list:
        """List all available reporters"""
        return list(self._reporters.keys())
    
    def create(self, name: str, config: Optional[Dict[str, Any]] = None) -> BaseReporter:
        """Create a reporter instance"""
        reporter_class = self.get(name)
        if reporter_class is None:
            raise ValueError(f"Unknown reporter: {name}")
        return reporter_class(config)


# Global reporter registry
reporter_registry = ReporterRegistry()