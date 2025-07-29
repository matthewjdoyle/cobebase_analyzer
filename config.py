"""
Configuration settings for the Codebase Analyzer
"""

import os
from typing import Dict, List, Any

# Default configuration
DEFAULT_CONFIG = {
    # Analysis settings
    'max_file_size_mb': 100,  # Skip files larger than this
    'max_depth': None,  # None means unlimited depth
    'follow_symlinks': False,
    'include_hidden': False,
    
    # Output settings
    'show_progress': True,
    'color_output': True,
    'detailed_by_default': False,
    
    # File type settings
    'text_file_extensions': {
        '.txt', '.md', '.rst', '.log', '.csv', '.tsv', '.json', '.xml',
        '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.env',
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c',
        '.cs', '.go', '.rs', '.php', '.rb', '.swift', '.kt', '.scala',
        '.r', '.m', '.pl', '.lua', '.sh', '.ps1', '.bat', '.vbs',
        '.sql', '.hs', '.ml', '.f90', '.asm', '.s', '.html', '.htm',
        '.css', '.scss', '.sass', '.less', '.svg'
    },
    
    # Binary file extensions (will be skipped for line counting)
    'binary_extensions': {
        '.exe', '.dll', '.so', '.dylib', '.pyc', '.pyo', '.jar',
        '.war', '.ear', '.apk', '.ipa', '.deb', '.rpm', '.tar',
        '.gz', '.zip', '.7z', '.rar', '.bz2', '.xz', '.jpg', '.jpeg',
        '.png', '.gif', '.bmp', '.tiff', '.ico', '.mp3', '.wav',
        '.mp4', '.avi', '.mov', '.pdf', '.doc', '.docx', '.rtf'
    },
    
    # Comment patterns for different languages
    'comment_patterns': {
        'Python': {'single': '#', 'multi_start': '"""', 'multi_end': '"""'},
        'JavaScript': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
        'TypeScript': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
        'Java': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
        'C++': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
        'C': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
        'C#': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
        'Go': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
        'Rust': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
        'PHP': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
        'Ruby': {'single': '#', 'multi_start': '=begin', 'multi_end': '=end'},
        'Swift': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
        'Kotlin': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
        'Scala': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
        'R': {'single': '#', 'multi_start': None, 'multi_end': None},
        'Objective-C': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
        'Perl': {'single': '#', 'multi_start': '=pod', 'multi_end': '=cut'},
        'Lua': {'single': '--', 'multi_start': '--[[', 'multi_end': ']]'},
        'Shell': {'single': '#', 'multi_start': None, 'multi_end': None},
        'PowerShell': {'single': '#', 'multi_start': '<#', 'multi_end': '#>'},
        'Batch': {'single': 'REM', 'multi_start': None, 'multi_end': None},
        'VBScript': {'single': "'", 'multi_start': None, 'multi_end': None},
        'SQL': {'single': '--', 'multi_start': '/*', 'multi_end': '*/'},
        'Haskell': {'single': '--', 'multi_start': '{-', 'multi_end': '-}'},
        'OCaml': {'single': '(*', 'multi_start': '(*', 'multi_end': '*)'},
        'Fortran': {'single': '!', 'multi_start': None, 'multi_end': None},
        'Assembly': {'single': ';', 'multi_start': None, 'multi_end': None},
        'HTML': {'single': None, 'multi_start': '<!--', 'multi_end': '-->'},
        'CSS': {'single': None, 'multi_start': '/*', 'multi_end': '*/'},
        'SCSS': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
        'SASS': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
        'LESS': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
        'XML': {'single': None, 'multi_start': '<!--', 'multi_end': '-->'},
        'YAML': {'single': '#', 'multi_start': None, 'multi_end': None},
        'TOML': {'single': '#', 'multi_start': None, 'multi_end': None},
        'INI': {'single': ';', 'multi_start': None, 'multi_end': None},
        'JSON': {'single': None, 'multi_start': None, 'multi_end': None},
        'Markdown': {'single': None, 'multi_start': None, 'multi_end': None},
        'reStructuredText': {'single': '..', 'multi_start': None, 'multi_end': None},
        'Text': {'single': None, 'multi_start': None, 'multi_end': None}
    },
    
    # Complexity metrics settings
    'complexity_metrics': {
        'enabled': True,
        'max_function_length': 50,
        'max_class_length': 500,
        'max_file_length': 1000,
        'cyclomatic_complexity_threshold': 10
    },
    
    # Export settings
    'export_formats': ['json', 'csv', 'txt', 'html'],
    'export_directory': 'reports',
    'include_timestamp': True,
    
    # Performance settings
    'parallel_processing': False,
    'max_workers': 4,
    'chunk_size': 1000
}

def load_config(config_file: str = None) -> Dict[str, Any]:
    """Load configuration from file or return defaults"""
    if config_file and os.path.exists(config_file):
        try:
            import json
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                # Merge with defaults
                config = DEFAULT_CONFIG.copy()
                config.update(user_config)
                return config
        except Exception as e:
            print(f"Warning: Could not load config file {config_file}: {e}")
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(config: Dict[str, Any], config_file: str) -> None:
    """Save configuration to file"""
    try:
        import json
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"Error saving config file: {e}")

def get_comment_patterns_for_file(file_path: str) -> Dict[str, str]:
    """Get comment patterns for a specific file based on its extension"""
    from pathlib import Path
    
    ext = Path(file_path).suffix.lower()
    file_type = None
    
    # Map extension to file type
    extension_to_type = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'React JSX',
        '.tsx': 'React TSX',
        '.java': 'Java',
        '.cpp': 'C++',
        '.c': 'C',
        '.cs': 'C#',
        '.go': 'Go',
        '.rs': 'Rust',
        '.php': 'PHP',
        '.rb': 'Ruby',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.r': 'R',
        '.m': 'Objective-C',
        '.pl': 'Perl',
        '.lua': 'Lua',
        '.sh': 'Shell',
        '.ps1': 'PowerShell',
        '.bat': 'Batch',
        '.vbs': 'VBScript',
        '.sql': 'SQL',
        '.hs': 'Haskell',
        '.ml': 'OCaml',
        '.f90': 'Fortran',
        '.asm': 'Assembly',
        '.s': 'Assembly',
        '.html': 'HTML',
        '.htm': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.sass': 'SASS',
        '.less': 'LESS',
        '.xml': 'XML',
        '.svg': 'SVG',
        '.json': 'JSON',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.toml': 'TOML',
        '.ini': 'INI',
        '.md': 'Markdown',
        '.rst': 'reStructuredText',
        '.txt': 'Text'
    }
    
    file_type = extension_to_type.get(ext, 'Text')
    return DEFAULT_CONFIG['comment_patterns'].get(file_type, {'single': None, 'multi_start': None, 'multi_end': None})

def is_text_file(file_path: str) -> bool:
    """Check if a file is a text file based on its extension"""
    from pathlib import Path
    ext = Path(file_path).suffix.lower()
    return ext in DEFAULT_CONFIG['text_file_extensions']

def is_binary_file(file_path: str) -> bool:
    """Check if a file is a binary file based on its extension"""
    from pathlib import Path
    ext = Path(file_path).suffix.lower()
    return ext in DEFAULT_CONFIG['binary_extensions']