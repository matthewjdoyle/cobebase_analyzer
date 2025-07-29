"""
JSON exporter implementation
"""

import json
from typing import Optional, Dict, Any, Union
from pathlib import Path

from .base import BaseExporter
from ..core.models import AnalysisResult

# Register this exporter
from .base import exporter_registry


class JSONExporter(BaseExporter):
    """JSON exporter for analysis results"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
    
    def export(self, result: AnalysisResult, output_path: Union[str, Path]) -> None:
        """Export analysis results to JSON file"""
        output_path = self.validate_output_path(output_path)
        
        # Format data for export
        export_data = self.format_data_for_export(result)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
    
    def get_supported_formats(self) -> list:
        """Get list of supported file formats"""
        return ['json']
    
    def format_data_for_export(self, result: AnalysisResult) -> Dict[str, Any]:
        """Format analysis result data for JSON export"""
        data = super().format_data_for_export(result)
        
        # Add additional JSON-specific formatting
        data['export_format'] = 'json'
        data['export_version'] = '2.0.0'
        
        # Convert datetime objects to ISO format strings
        if 'analysis_date' in data:
            data['analysis_date'] = result.analysis_date.isoformat()
        
        # Add file details with proper datetime handling
        data['files'] = []
        for file_info in result.files:
            file_data = file_info.dict()
            if file_info.last_modified:
                file_data['last_modified'] = file_info.last_modified.isoformat()
            data['files'].append(file_data)
        
        # Add largest files with proper datetime handling
        data['largest_files'] = []
        for file_info in result.largest_files:
            file_data = file_info.dict()
            if file_info.last_modified:
                file_data['last_modified'] = file_info.last_modified.isoformat()
            data['largest_files'].append(file_data)
        
        return data


# Register the JSON exporter
exporter_registry.register('json', JSONExporter)