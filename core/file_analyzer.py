"""
File analysis functionality for individual files
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional

from utils.file_utils import get_file_type, is_text_file


class FileAnalyzer:
    """Analyzes individual files for metrics"""
    
    def analyze_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze a single file and return metrics"""
        try:
            stat = file_path.stat()
            file_size = stat.st_size
            file_type = get_file_type(file_path)
            
            # Count lines
            lines = 0
            code_lines = 0
            comment_lines = 0
            blank_lines = 0
            
            # Only try to read text files
            if is_text_file(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            lines += 1
                            stripped = line.strip()
                            
                            if not stripped:
                                blank_lines += 1
                            elif self._is_comment_line(stripped, file_type):
                                comment_lines += 1
                            else:
                                code_lines += 1
                except (UnicodeDecodeError, PermissionError, OSError):
                    # Binary file or permission denied
                    lines = code_lines = comment_lines = blank_lines = 0
            
            return {
                'path': str(file_path),
                'name': file_path.name,
                'type': file_type,
                'size': file_size,
                'lines': lines,
                'code_lines': code_lines,
                'comment_lines': comment_lines,
                'blank_lines': blank_lines,
                'extension': file_path.suffix.lower()
            }
        except (PermissionError, OSError):
            return None
    
    def _is_comment_line(self, line: str, file_type: str) -> bool:
        """Check if a line is a comment based on file type"""
        comment_patterns = {
            'Python': ['#'],
            'JavaScript': ['//', '/*', '*/', '*'],
            'TypeScript': ['//', '/*', '*/', '*'],
            'Java': ['//', '/*', '*/', '*'],
            'C++': ['//', '/*', '*/', '*'],
            'C': ['//', '/*', '*/', '*'],
            'C#': ['//', '/*', '*/', '*'],
            'Go': ['//', '/*', '*/', '*'],
            'Rust': ['//', '/*', '*/', '*'],
            'PHP': ['//', '/*', '*/', '*', '#'],
            'Ruby': ['#'],
            'Shell': ['#'],
            'CSS': ['/*', '*/', '*'],
            'HTML': ['<!--', '-->'],
            'XML': ['<!--', '-->'],
            'SQL': ['--', '/*', '*/', '*'],
            'Markdown': ['<!--', '-->']
        }
        
        patterns = comment_patterns.get(file_type, [])
        return any(line.startswith(pattern) for pattern in patterns)