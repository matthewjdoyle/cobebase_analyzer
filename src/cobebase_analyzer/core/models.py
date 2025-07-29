"""
Core data models for the Codebase Analyzer
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from collections import defaultdict
from pydantic import BaseModel, Field, validator
import json


class FileInfo(BaseModel):
    """Information about a single file"""
    path: str = Field(..., description="Full path to the file")
    name: str = Field(..., description="File name")
    type: str = Field(..., description="File type/category")
    size: int = Field(..., description="File size in bytes")
    lines: int = Field(0, description="Total number of lines")
    code_lines: int = Field(0, description="Number of code lines")
    comment_lines: int = Field(0, description="Number of comment lines")
    blank_lines: int = Field(0, description="Number of blank lines")
    extension: str = Field("", description="File extension")
    last_modified: Optional[datetime] = Field(None, description="Last modification time")
    
    @validator('path')
    def validate_path(cls, v):
        if not v:
            raise ValueError("Path cannot be empty")
        return str(Path(v).resolve())
    
    @property
    def size_mb(self) -> float:
        """File size in megabytes"""
        return self.size / (1024 * 1024)
    
    @property
    def size_kb(self) -> float:
        """File size in kilobytes"""
        return self.size / 1024
    
    @property
    def comment_ratio(self) -> float:
        """Ratio of comments to total lines"""
        total = self.code_lines + self.comment_lines
        return (self.comment_lines / total * 100) if total > 0 else 0.0


class ProjectStats(BaseModel):
    """Project-level statistics"""
    total_files: int = Field(0, description="Total number of files")
    total_dirs: int = Field(0, description="Total number of directories")
    total_lines: int = Field(0, description="Total lines of code")
    total_size: int = Field(0, description="Total size in bytes")
    file_types: Dict[str, int] = Field(default_factory=dict, description="Count by file type")
    file_sizes: Dict[str, int] = Field(default_factory=dict, description="Size by file type")
    lines_by_type: Dict[str, int] = Field(default_factory=dict, description="Lines by file type")
    
    @property
    def total_size_mb(self) -> float:
        """Total size in megabytes"""
        return self.total_size / (1024 * 1024)
    
    @property
    def unique_file_types(self) -> int:
        """Number of unique file types"""
        return len(self.file_types)
    
    @property
    def average_file_size(self) -> float:
        """Average file size in bytes"""
        return self.total_size / self.total_files if self.total_files > 0 else 0
    
    @property
    def average_lines_per_file(self) -> float:
        """Average lines per file"""
        return self.total_lines / self.total_files if self.total_files > 0 else 0


class AnalysisResult(BaseModel):
    """Complete analysis result"""
    project_path: str = Field(..., description="Path to the analyzed project")
    analysis_date: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")
    stats: ProjectStats = Field(..., description="Project statistics")
    files: List[FileInfo] = Field(default_factory=list, description="Detailed file information")
    largest_files: List[FileInfo] = Field(default_factory=list, description="Largest files by size")
    analysis_duration: float = Field(0.0, description="Analysis duration in seconds")
    config: Dict[str, Any] = Field(default_factory=dict, description="Configuration used")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Path: lambda v: str(v)
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.dict()
    
    def to_json(self, **kwargs) -> str:
        """Convert to JSON string"""
        return self.json(**kwargs)
    
    def save_json(self, filepath: Union[str, Path]) -> None:
        """Save to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json(indent=2))
    
    @classmethod
    def from_json(cls, filepath: Union[str, Path]) -> 'AnalysisResult':
        """Load from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(**data)
    
    def get_files_by_type(self, file_type: str) -> List[FileInfo]:
        """Get all files of a specific type"""
        return [f for f in self.files if f.type == file_type]
    
    def get_largest_files(self, limit: int = 10) -> List[FileInfo]:
        """Get the largest files, limited by count"""
        return sorted(self.files, key=lambda x: x.size, reverse=True)[:limit]
    
    def get_most_complex_files(self, limit: int = 10) -> List[FileInfo]:
        """Get files with the most lines, limited by count"""
        return sorted(self.files, key=lambda x: x.lines, reverse=True)[:limit]


@dataclass
class AnalysisContext:
    """Context for analysis operations"""
    project_path: Path
    config: Dict[str, Any]
    ignore_patterns: List[str]
    max_depth: Optional[int]
    follow_symlinks: bool = False
    include_hidden: bool = False
    
    def __post_init__(self):
        if isinstance(self.project_path, str):
            self.project_path = Path(self.project_path)


@dataclass
class AnalysisProgress:
    """Progress tracking for analysis operations"""
    total_items: int = 0
    processed_items: int = 0
    current_file: Optional[str] = None
    start_time: Optional[datetime] = None
    estimated_remaining: Optional[float] = None
    
    @property
    def progress_percentage(self) -> float:
        """Progress as percentage"""
        if self.total_items == 0:
            return 0.0
        return (self.processed_items / self.total_items) * 100
    
    @property
    def elapsed_time(self) -> Optional[float]:
        """Elapsed time in seconds"""
        if self.start_time is None:
            return None
        return (datetime.now() - self.start_time).total_seconds()


class FileTypeRegistry:
    """Registry for file type detection and handling"""
    
    def __init__(self):
        self._extensions: Dict[str, str] = {}
        self._mime_types: Dict[str, str] = {}
        self._patterns: Dict[str, str] = {}
        self._load_defaults()
    
    def _load_defaults(self):
        """Load default file type mappings"""
        # Programming Languages
        lang_extensions = {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
            '.jsx': 'React JSX', '.tsx': 'React TSX', '.java': 'Java',
            '.cpp': 'C++', '.c': 'C', '.cs': 'C#', '.go': 'Go',
            '.rs': 'Rust', '.php': 'PHP', '.rb': 'Ruby', '.swift': 'Swift',
            '.kt': 'Kotlin', '.scala': 'Scala', '.r': 'R', '.m': 'Objective-C',
            '.pl': 'Perl', '.lua': 'Lua', '.sh': 'Shell', '.ps1': 'PowerShell',
            '.bat': 'Batch', '.vbs': 'VBScript', '.sql': 'SQL',
            '.hs': 'Haskell', '.ml': 'OCaml', '.f90': 'Fortran',
            '.asm': 'Assembly', '.s': 'Assembly'
        }
        
        # Web Technologies
        web_extensions = {
            '.html': 'HTML', '.htm': 'HTML', '.css': 'CSS',
            '.scss': 'SCSS', '.sass': 'SASS', '.less': 'LESS',
            '.xml': 'XML', '.svg': 'SVG'
        }
        
        # Configuration & Data
        config_extensions = {
            '.json': 'JSON', '.yaml': 'YAML', '.yml': 'YAML',
            '.toml': 'TOML', '.ini': 'INI', '.cfg': 'Config',
            '.conf': 'Config', '.env': 'Environment',
            '.properties': 'Properties', '.lock': 'Lock File'
        }
        
        # Documentation
        doc_extensions = {
            '.md': 'Markdown', '.rst': 'reStructuredText',
            '.txt': 'Text', '.pdf': 'PDF', '.doc': 'Word',
            '.docx': 'Word', '.rtf': 'Rich Text'
        }
        
        self._extensions.update(lang_extensions)
        self._extensions.update(web_extensions)
        self._extensions.update(config_extensions)
        self._extensions.update(doc_extensions)
    
    def register_extension(self, extension: str, file_type: str) -> None:
        """Register a new file extension mapping"""
        self._extensions[extension.lower()] = file_type
    
    def get_file_type(self, file_path: Union[str, Path]) -> str:
        """Get file type based on extension"""
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        ext = file_path.suffix.lower()
        return self._extensions.get(ext, 'Unknown')
    
    def get_extensions_for_type(self, file_type: str) -> List[str]:
        """Get all extensions for a file type"""
        return [ext for ext, type_name in self._extensions.items() if type_name == file_type]
    
    def list_file_types(self) -> List[str]:
        """List all registered file types"""
        return list(set(self._extensions.values()))


# Global file type registry instance
file_type_registry = FileTypeRegistry()