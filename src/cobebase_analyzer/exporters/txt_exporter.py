"""
Text exporter implementation
"""

from typing import Optional, Dict, Any, Union
from pathlib import Path

from .base import BaseExporter
from ..core.models import AnalysisResult

# Register this exporter
from .base import exporter_registry


class TextExporter(BaseExporter):
    """Text exporter for analysis results"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
    
    def export(self, result: AnalysisResult, output_path: Union[str, Path]) -> None:
        """Export analysis results to text file"""
        output_path = self.validate_output_path(output_path)
        
        # Generate text report
        from ..reporters.text_reporter import TextReporter
        reporter = TextReporter()
        report_text = reporter.generate_report(result, detailed=True)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
    
    def get_supported_formats(self) -> list:
        """Get list of supported file formats"""
        return ['txt', 'text']