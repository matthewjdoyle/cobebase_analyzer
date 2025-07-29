"""
Base exporter interface for the Codebase Analyzer
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Union
from pathlib import Path
from ..core.models import AnalysisResult


class BaseExporter(ABC):
    """Base class for all exporters"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
    
    @abstractmethod
    def export(self, result: AnalysisResult, output_path: Union[str, Path]) -> None:
        """Export analysis results to the specified path"""
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> list:
        """Get list of supported file formats"""
        pass
    
    def validate_output_path(self, output_path: Union[str, Path]) -> Path:
        """Validate and prepare output path"""
        if isinstance(output_path, str):
            output_path = Path(output_path)
        
        # Create parent directories if they don't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        return output_path
    
    def get_default_filename(self, result: AnalysisResult, extension: str) -> str:
        """Generate a default filename for export"""
        from datetime import datetime
        
        project_name = Path(result.project_path).name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"codebase_analysis_{project_name}_{timestamp}.{extension}"
    
    def format_data_for_export(self, result: AnalysisResult) -> Dict[str, Any]:
        """Format analysis result data for export"""
        return {
            'project_path': result.project_path,
            'analysis_date': result.analysis_date.isoformat(),
            'analysis_duration': result.analysis_duration,
            'config': result.config,
            'summary': {
                'total_files': result.stats.total_files,
                'total_directories': result.stats.total_dirs,
                'total_lines': result.stats.total_lines,
                'total_size': result.stats.total_size,
                'total_size_mb': result.stats.total_size_mb,
                'unique_file_types': result.stats.unique_file_types,
                'average_file_size': result.stats.average_file_size,
                'average_lines_per_file': result.stats.average_lines_per_file
            },
            'file_types': result.stats.file_types,
            'file_sizes': result.stats.file_sizes,
            'lines_by_type': result.stats.lines_by_type,
            'files': [file.dict() for file in result.files],
            'largest_files': [file.dict() for file in result.largest_files]
        }


class ExporterRegistry:
    """Registry for managing different exporter types"""
    
    def __init__(self):
        self._exporters: Dict[str, type] = {}
    
    def register(self, name: str, exporter_class: type) -> None:
        """Register a new exporter"""
        if not issubclass(exporter_class, BaseExporter):
            raise ValueError(f"Exporter class must inherit from BaseExporter")
        self._exporters[name] = exporter_class
    
    def get(self, name: str) -> Optional[type]:
        """Get an exporter by name"""
        return self._exporters.get(name)
    
    def list_available(self) -> list:
        """List all available exporters"""
        return list(self._exporters.keys())
    
    def create(self, name: str, config: Optional[Dict[str, Any]] = None) -> BaseExporter:
        """Create an exporter instance"""
        exporter_class = self.get(name)
        if exporter_class is None:
            raise ValueError(f"Unknown exporter: {name}")
        return exporter_class(config)
    
    def get_exporter_for_format(self, format_name: str) -> Optional[BaseExporter]:
        """Get exporter for a specific format"""
        for name, exporter_class in self._exporters.items():
            exporter = exporter_class()
            if format_name.lower() in exporter.get_supported_formats():
                return exporter
        return None


# Global exporter registry
exporter_registry = ExporterRegistry()