"""
File utility functions and constants
"""

from pathlib import Path
from typing import Dict, List, Set

# File type mappings
FILE_EXTENSIONS = {
    # Programming Languages
    '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript', '.jsx': 'React JSX',
    '.tsx': 'React TSX', '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.cs': 'C#',
    '.go': 'Go', '.rs': 'Rust', '.php': 'PHP', '.rb': 'Ruby', '.swift': 'Swift',
    '.kt': 'Kotlin', '.scala': 'Scala', '.r': 'R', '.m': 'Objective-C',
    '.pl': 'Perl', '.lua': 'Lua', '.sh': 'Shell', '.ps1': 'PowerShell',
    '.bat': 'Batch', '.vbs': 'VBScript', '.sql': 'SQL', '.hs': 'Haskell',
    '.ml': 'OCaml', '.f90': 'Fortran', '.asm': 'Assembly', '.s': 'Assembly',
    
    # Web Technologies
    '.html': 'HTML', '.htm': 'HTML', '.css': 'CSS', '.scss': 'SCSS',
    '.sass': 'SASS', '.less': 'LESS', '.xml': 'XML', '.svg': 'SVG',
    
    # Configuration & Data
    '.json': 'JSON', '.yaml': 'YAML', '.yml': 'YAML', '.toml': 'TOML',
    '.ini': 'INI', '.cfg': 'Config', '.conf': 'Config', '.env': 'Environment',
    '.properties': 'Properties', '.lock': 'Lock File', '.log': 'Log',
    
    # Documentation
    '.md': 'Markdown', '.rst': 'reStructuredText', '.txt': 'Text',
    '.pdf': 'PDF', '.doc': 'Word', '.docx': 'Word', '.rtf': 'Rich Text',
    
    # Build & Package
    '.pyc': 'Python Bytecode', '.pyo': 'Python Bytecode', '.so': 'Shared Object',
    '.dll': 'Dynamic Library', '.exe': 'Executable', '.jar': 'Java Archive',
    '.war': 'Web Archive', '.ear': 'Enterprise Archive', '.apk': 'Android Package',
    '.ipa': 'iOS Package', '.deb': 'Debian Package', '.rpm': 'RPM Package',
    '.tar': 'Archive', '.gz': 'Compressed', '.zip': 'Archive', '.7z': 'Archive',
    '.rar': 'Archive', '.bz2': 'Compressed', '.xz': 'Compressed',
    
    # Media
    '.jpg': 'Image', '.jpeg': 'Image', '.png': 'Image', '.gif': 'Image',
    '.bmp': 'Image', '.tiff': 'Image', '.ico': 'Icon', '.mp3': 'Audio',
    '.wav': 'Audio', '.mp4': 'Video', '.avi': 'Video', '.mov': 'Video',
    
    # Version Control
    '.git': 'Git Repository', '.gitignore': 'Git Ignore', '.gitattributes': 'Git Attributes',
    
    # IDE & Editor
    '.vscode': 'VS Code', '.idea': 'IntelliJ IDEA', '.sublime-project': 'Sublime Text',
    '.vim': 'Vim', '.emacs': 'Emacs', '.swp': 'Vim Swap', '.swo': 'Vim Swap',
    
    # Other
    '.bak': 'Backup', '.tmp': 'Temporary', '.cache': 'Cache', '.db': 'Database',
    '.sqlite': 'SQLite Database', '.sqlite3': 'SQLite Database'
}

# Common ignore patterns
DEFAULT_IGNORE_PATTERNS = [
    '__pycache__', '.git', '.svn', '.hg', '.DS_Store', 'Thumbs.db',
    'node_modules', 'venv', 'env', '.venv', '.env', 'dist', 'build',
    '*.pyc', '*.pyo', '*.so', '*.dll', '*.exe', '*.log', '*.tmp',
    '.pytest_cache', '.coverage', '.tox', '.mypy_cache'
]


def get_file_type(file_path: Path) -> str:
    """Determine file type based on extension"""
    ext = file_path.suffix.lower()
    return FILE_EXTENSIONS.get(ext, 'Unknown')


def should_ignore_path(path: Path, ignore_patterns: List[str]) -> bool:
    """Check if path should be ignored based on patterns"""
    path_str = str(path)
    for pattern in ignore_patterns:
        if pattern.startswith('*'):
            if path_str.endswith(pattern[1:]):
                return True
        elif pattern in path_str:
            return True
    return False


def is_text_file(file_path: Path) -> bool:
    """Check if file is likely a text file based on extension"""
    text_extensions = {
        '.txt', '.md', '.rst', '.log', '.csv', '.tsv', '.json', '.xml',
        '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.env',
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c',
        '.cs', '.go', '.rs', '.php', '.rb', '.swift', '.kt', '.scala',
        '.r', '.m', '.pl', '.lua', '.sh', '.ps1', '.bat', '.vbs',
        '.sql', '.hs', '.ml', '.f90', '.asm', '.s', '.html', '.htm',
        '.css', '.scss', '.sass', '.less', '.svg'
    }
    return file_path.suffix.lower() in text_extensions


def format_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"