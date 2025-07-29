"""
CSV exporter implementation
"""

import csv
from typing import Optional, Dict, Any, Union
from pathlib import Path

from .base import BaseExporter
from ..core.models import AnalysisResult

# Register this exporter
from .base import exporter_registry


class CSVExporter(BaseExporter):
    """CSV exporter for analysis results"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
    
    def export(self, result: AnalysisResult, output_path: Union[str, Path]) -> None:
        """Export analysis results to CSV file"""
        output_path = self.validate_output_path(output_path)
        
        # Create CSV files for different aspects of the analysis
        base_path = output_path.with_suffix('')
        
        # Export file types summary
        self._export_file_types_summary(result, f"{base_path}_file_types.csv")
        
        # Export individual files
        self._export_files_details(result, f"{base_path}_files.csv")
        
        # Export largest files
        self._export_largest_files(result, f"{base_path}_largest_files.csv")
        
        # Export summary statistics
        self._export_summary_stats(result, f"{base_path}_summary.csv")
    
    def get_supported_formats(self) -> list:
        """Get list of supported file formats"""
        return ['csv']
    
    def _export_file_types_summary(self, result: AnalysisResult, output_path: Union[str, Path]) -> None:
        """Export file types summary to CSV"""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'File Type', 'Count', 'Lines', 'Size (bytes)', 'Size (MB)', 
                'Percentage of Total Files'
            ])
            
            stats = result.stats
            total_files = stats.total_files
            
            for file_type, count in stats.file_types.items():
                lines = stats.lines_by_type.get(file_type, 0)
                size = stats.file_sizes.get(file_type, 0)
                size_mb = size / (1024 * 1024)
                percentage = (count / total_files * 100) if total_files > 0 else 0
                
                writer.writerow([
                    file_type, count, lines, size, f"{size_mb:.2f}", f"{percentage:.1f}"
                ])
    
    def _export_files_details(self, result: AnalysisResult, output_path: Union[str, Path]) -> None:
        """Export detailed file information to CSV"""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'File Path', 'File Name', 'File Type', 'Extension', 'Size (bytes)',
                'Size (KB)', 'Size (MB)', 'Total Lines', 'Code Lines', 
                'Comment Lines', 'Blank Lines', 'Comment Ratio (%)', 'Last Modified'
            ])
            
            for file_info in result.files:
                writer.writerow([
                    file_info.path,
                    file_info.name,
                    file_info.type,
                    file_info.extension,
                    file_info.size,
                    f"{file_info.size_kb:.1f}",
                    f"{file_info.size_mb:.2f}",
                    file_info.lines,
                    file_info.code_lines,
                    file_info.comment_lines,
                    file_info.blank_lines,
                    f"{file_info.comment_ratio:.1f}",
                    file_info.last_modified.isoformat() if file_info.last_modified else ''
                ])
    
    def _export_largest_files(self, result: AnalysisResult, output_path: Union[str, Path]) -> None:
        """Export largest files to CSV"""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Rank', 'File Name', 'File Type', 'Size (bytes)', 'Size (MB)',
                'Total Lines', 'Code Lines', 'Comment Lines', 'Blank Lines'
            ])
            
            largest_files = result.get_largest_files(20)  # Top 20 largest files
            
            for i, file_info in enumerate(largest_files, 1):
                writer.writerow([
                    i,
                    file_info.name,
                    file_info.type,
                    file_info.size,
                    f"{file_info.size_mb:.2f}",
                    file_info.lines,
                    file_info.code_lines,
                    file_info.comment_lines,
                    file_info.blank_lines
                ])
    
    def _export_summary_stats(self, result: AnalysisResult, output_path: Union[str, Path]) -> None:
        """Export summary statistics to CSV"""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Metric', 'Value'])
            
            stats = result.stats
            writer.writerow(['Project Path', result.project_path])
            writer.writerow(['Analysis Date', result.analysis_date.isoformat()])
            writer.writerow(['Analysis Duration (seconds)', f"{result.analysis_duration:.2f}"])
            writer.writerow(['Total Files', stats.total_files])
            writer.writerow(['Total Directories', stats.total_dirs])
            writer.writerow(['Total Lines of Code', stats.total_lines])
            writer.writerow(['Total Size (bytes)', stats.total_size])
            writer.writerow(['Total Size (MB)', f"{stats.total_size_mb:.2f}"])
            writer.writerow(['Unique File Types', stats.unique_file_types])
            writer.writerow(['Average File Size (bytes)', f"{stats.average_file_size:.1f}"])
            writer.writerow(['Average Lines per File', f"{stats.average_lines_per_file:.1f}"])
    
    def get_default_filename(self, result: AnalysisResult, extension: str) -> str:
        """Generate a default filename for CSV export"""
        # For CSV, we'll create multiple files, so use a base name
        from datetime import datetime
        
        project_name = Path(result.project_path).name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"codebase_analysis_{project_name}_{timestamp}"


# Register the CSV exporter
exporter_registry.register('csv', CSVExporter)