"""
Configuration management for the Codebase Analyzer
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, validator, root_validator
from dataclasses import dataclass


class CommentPatterns(BaseModel):
    """Comment patterns for different programming languages"""
    single: Optional[str] = Field(None, description="Single-line comment pattern")
    multi_start: Optional[str] = Field(None, description="Multi-line comment start pattern")
    multi_end: Optional[str] = Field(None, description="Multi-line comment end pattern")


class ComplexityMetrics(BaseModel):
    """Complexity analysis configuration"""
    enabled: bool = Field(True, description="Enable complexity analysis")
    max_function_length: int = Field(50, description="Maximum function length")
    max_class_length: int = Field(500, description="Maximum class length")
    max_file_length: int = Field(1000, description="Maximum file length")
    cyclomatic_complexity_threshold: int = Field(10, description="Cyclomatic complexity threshold")


class ExportSettings(BaseModel):
    """Export configuration"""
    formats: List[str] = Field(default_factory=lambda: ['json', 'csv', 'txt'], description="Supported export formats")
    directory: str = Field('reports', description="Default export directory")
    include_timestamp: bool = Field(True, description="Include timestamp in export filenames")
    compression: bool = Field(False, description="Enable compression for exports")


class PerformanceSettings(BaseModel):
    """Performance optimization settings"""
    parallel_processing: bool = Field(False, description="Enable parallel processing")
    max_workers: int = Field(4, description="Maximum number of worker processes")
    chunk_size: int = Field(1000, description="Chunk size for batch processing")
    memory_limit_mb: int = Field(512, description="Memory limit in MB")


class Config(BaseModel):
    """Main configuration class"""
    
    # Analysis settings
    max_file_size_mb: int = Field(100, description="Skip files larger than this size")
    max_depth: Optional[int] = Field(None, description="Maximum directory depth to analyze")
    follow_symlinks: bool = Field(False, description="Follow symbolic links")
    include_hidden: bool = Field(False, description="Include hidden files and directories")
    
    # Output settings
    show_progress: bool = Field(True, description="Show progress indicators")
    color_output: bool = Field(True, description="Enable colored output")
    detailed_by_default: bool = Field(False, description="Show detailed output by default")
    quiet_mode: bool = Field(False, description="Suppress non-essential output")
    
    # File type settings
    text_file_extensions: List[str] = Field(
        default_factory=lambda: [
            '.txt', '.md', '.rst', '.log', '.csv', '.tsv', '.json', '.xml',
            '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.env',
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c',
            '.cs', '.go', '.rs', '.php', '.rb', '.swift', '.kt', '.scala',
            '.r', '.m', '.pl', '.lua', '.sh', '.ps1', '.bat', '.vbs',
            '.sql', '.hs', '.ml', '.f90', '.asm', '.s', '.html', '.htm',
            '.css', '.scss', '.sass', '.less', '.svg'
        ],
        description="Extensions considered as text files"
    )
    
    binary_extensions: List[str] = Field(
        default_factory=lambda: [
            '.exe', '.dll', '.so', '.dylib', '.pyc', '.pyo', '.jar',
            '.war', '.ear', '.apk', '.ipa', '.deb', '.rpm', '.tar',
            '.gz', '.zip', '.7z', '.rar', '.bz2', '.xz', '.jpg', '.jpeg',
            '.png', '.gif', '.bmp', '.tiff', '.ico', '.mp3', '.wav',
            '.mp4', '.avi', '.mov', '.pdf', '.doc', '.docx', '.rtf'
        ],
        description="Extensions considered as binary files"
    )
    
    # Comment patterns
    comment_patterns: Dict[str, CommentPatterns] = Field(
        default_factory=lambda: {
            'Python': CommentPatterns(single='#', multi_start='"""', multi_end='"""'),
            'JavaScript': CommentPatterns(single='//', multi_start='/*', multi_end='*/'),
            'TypeScript': CommentPatterns(single='//', multi_start='/*', multi_end='*/'),
            'Java': CommentPatterns(single='//', multi_start='/*', multi_end='*/'),
            'C++': CommentPatterns(single='//', multi_start='/*', multi_end='*/'),
            'C': CommentPatterns(single='//', multi_start='/*', multi_end='*/'),
            'C#': CommentPatterns(single='//', multi_start='/*', multi_end='*/'),
            'Go': CommentPatterns(single='//', multi_start='/*', multi_end='*/'),
            'Rust': CommentPatterns(single='//', multi_start='/*', multi_end='*/'),
            'PHP': CommentPatterns(single='//', multi_start='/*', multi_end='*/'),
            'Ruby': CommentPatterns(single='#', multi_start='=begin', multi_end='=end'),
            'Swift': CommentPatterns(single='//', multi_start='/*', multi_end='*/'),
            'Kotlin': CommentPatterns(single='//', multi_start='/*', multi_end='*/'),
            'Scala': CommentPatterns(single='//', multi_start='/*', multi_end='*/'),
            'R': CommentPatterns(single='#'),
            'Objective-C': CommentPatterns(single='//', multi_start='/*', multi_end='*/'),
            'Perl': CommentPatterns(single='#', multi_start='=pod', multi_end='=cut'),
            'Lua': CommentPatterns(single='--', multi_start='--[[', multi_end=']]'),
            'Shell': CommentPatterns(single='#'),
            'PowerShell': CommentPatterns(single='#', multi_start='<#', multi_end='#>'),
            'Batch': CommentPatterns(single='REM'),
            'VBScript': CommentPatterns(single="'"),
            'SQL': CommentPatterns(single='--', multi_start='/*', multi_end='*/'),
            'Haskell': CommentPatterns(single='--', multi_start='{-', multi_end='-}'),
            'OCaml': CommentPatterns(single='(*', multi_start='(*', multi_end='*)'),
            'Fortran': CommentPatterns(single='!'),
            'Assembly': CommentPatterns(single=';'),
            'HTML': CommentPatterns(multi_start='<!--', multi_end='-->'),
            'CSS': CommentPatterns(multi_start='/*', multi_end='*/'),
            'SCSS': CommentPatterns(single='//', multi_start='/*', multi_end='*/'),
            'SASS': CommentPatterns(single='//', multi_start='/*', multi_end='*/'),
            'LESS': CommentPatterns(single='//', multi_start='/*', multi_end='*/'),
            'XML': CommentPatterns(multi_start='<!--', multi_end='-->'),
            'YAML': CommentPatterns(single='#'),
            'TOML': CommentPatterns(single='#'),
            'INI': CommentPatterns(single=';'),
            'JSON': CommentPatterns(),
            'Markdown': CommentPatterns(),
            'reStructuredText': CommentPatterns(single='..'),
            'Text': CommentPatterns()
        },
        description="Comment patterns for different languages"
    )
    
    # Complexity metrics
    complexity_metrics: ComplexityMetrics = Field(
        default_factory=ComplexityMetrics,
        description="Complexity analysis configuration"
    )
    
    # Export settings
    export_settings: ExportSettings = Field(
        default_factory=ExportSettings,
        description="Export configuration"
    )
    
    # Performance settings
    performance: PerformanceSettings = Field(
        default_factory=PerformanceSettings,
        description="Performance optimization settings"
    )
    
    # Default ignore patterns
    default_ignore_patterns: List[str] = Field(
        default_factory=lambda: [
            '__pycache__', '.git', '.svn', '.hg', '.DS_Store', 'Thumbs.db',
            'node_modules', 'venv', 'env', '.venv', '.env', 'dist', 'build',
            '*.pyc', '*.pyo', '*.so', '*.dll', '*.exe', '*.log', '*.tmp',
            '.pytest_cache', '.coverage', '.tox', '.mypy_cache'
        ],
        description="Default patterns to ignore"
    )
    
    @validator('max_file_size_mb')
    def validate_max_file_size(cls, v):
        if v <= 0:
            raise ValueError("max_file_size_mb must be positive")
        return v
    
    @validator('max_depth')
    def validate_max_depth(cls, v):
        if v is not None and v < 0:
            raise ValueError("max_depth must be non-negative")
        return v
    
    @validator('performance')
    def validate_performance(cls, v):
        if v.max_workers <= 0:
            raise ValueError("max_workers must be positive")
        if v.chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        return v
    
    def get_comment_patterns_for_file(self, file_path: Union[str, Path]) -> CommentPatterns:
        """Get comment patterns for a specific file"""
        from .models import file_type_registry
        
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        file_type = file_type_registry.get_file_type(file_path)
        return self.comment_patterns.get(file_type, CommentPatterns())
    
    def is_text_file(self, file_path: Union[str, Path]) -> bool:
        """Check if a file is a text file based on its extension"""
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        ext = file_path.suffix.lower()
        return ext in self.text_file_extensions
    
    def is_binary_file(self, file_path: Union[str, Path]) -> bool:
        """Check if a file is a binary file based on its extension"""
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        ext = file_path.suffix.lower()
        return ext in self.binary_extensions
    
    def should_ignore_file(self, file_path: Union[str, Path], custom_ignore: List[str] = None) -> bool:
        """Check if a file should be ignored"""
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        path_str = str(file_path)
        ignore_patterns = self.default_ignore_patterns + (custom_ignore or [])
        
        for pattern in ignore_patterns:
            if pattern.startswith('*'):
                if path_str.endswith(pattern[1:]):
                    return True
            elif pattern in path_str:
                return True
        
        return False


def get_default_config_path() -> Path:
    """Get the default configuration file path"""
    return Path.home() / ".cobebase_analyzer.json"


def load_config(config_file: Union[str, Path] = None) -> Config:
    """Load configuration from file or return defaults"""
    if config_file is None:
        config_file = get_default_config_path()
    
    if isinstance(config_file, str):
        config_file = Path(config_file)
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle nested configuration updates
            config = Config()
            for key, value in data.items():
                if hasattr(config, key):
                    if isinstance(value, dict) and hasattr(getattr(config, key), 'dict'):
                        # Update nested models
                        current = getattr(config, key)
                        current_dict = current.dict()
                        current_dict.update(value)
                        setattr(config, key, type(current)(**current_dict))
                    else:
                        setattr(config, key, value)
            
            return config
        except Exception as e:
            print(f"Warning: Could not load config file {config_file}: {e}")
            return Config()
    
    return Config()


def save_config(config: Config, config_file: Union[str, Path] = None) -> None:
    """Save configuration to file"""
    if config_file is None:
        config_file = get_default_config_path()
    
    if isinstance(config_file, str):
        config_file = Path(config_file)
    
    try:
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config.dict(), f, indent=2, default=str)
    except Exception as e:
        raise RuntimeError(f"Error saving config file: {e}")


def create_default_config(config_file: Union[str, Path] = None) -> Config:
    """Create and save a default configuration file"""
    config = Config()
    save_config(config, config_file)
    return config


# Global configuration instance
_default_config = None


def get_config() -> Config:
    """Get the global configuration instance"""
    global _default_config
    if _default_config is None:
        _default_config = load_config()
    return _default_config


def set_config(config: Config) -> None:
    """Set the global configuration instance"""
    global _default_config
    _default_config = config