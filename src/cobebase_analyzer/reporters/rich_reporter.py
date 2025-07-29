"""
Rich reporter implementation for beautiful terminal output
"""

from typing import Optional, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich import box

from .base import BaseReporter
from ..core.models import AnalysisResult

# Register this reporter
from .base import reporter_registry


class RichReporter(BaseReporter):
    """Rich-based reporter for beautiful terminal output"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.console = Console()
    
    def generate_report(self, result: AnalysisResult, detailed: bool = False) -> str:
        """Generate a rich-formatted report string"""
        with self.console.capture() as capture:
            self.display_report(result, detailed)
        return capture.get()
    
    def display_report(self, result: AnalysisResult, detailed: bool = False) -> None:
        """Display a rich-formatted report to console"""
        # Summary table
        summary_table = self._create_summary_table(result)
        self.console.print(summary_table)
        self.console.print()
        
        # File types table
        file_types_table = self._create_file_types_table(result)
        self.console.print(file_types_table)
        self.console.print()
        
        # Project tree
        tree = self._create_project_tree(result)
        self.console.print(Panel.fit("🌳 Project Structure with File Statistics", style="bold blue"))
        self.console.print(tree)
        
        if detailed:
            self.console.print()
            
            # Largest files table
            largest_files_table = self._create_largest_files_table(result)
            self.console.print(largest_files_table)
            self.console.print()
            
            # Detailed metrics table
            detailed_table = self._create_detailed_metrics_table(result)
            self.console.print(detailed_table)
    
    def _create_summary_table(self, result: AnalysisResult) -> Table:
        """Create summary statistics table"""
        summary_stats = self.get_summary_stats(result)
        
        table = Table(title="📊 Codebase Analysis Summary", box=box.ROUNDED)
        table.add_column("Metric", style="cyan", no_wrap=True, width=20)
        table.add_column("Value", style="green", width=15)
        
        table.add_row("Total Files", str(summary_stats['total_files']))
        table.add_row("Total Directories", str(summary_stats['total_dirs']))
        table.add_row("Total Lines of Code", self.format_number(summary_stats['total_lines']))
        table.add_row("Total Size", f"{summary_stats['total_size_mb']:.2f} MB")
        table.add_row("Unique File Types", str(summary_stats['unique_file_types']))
        table.add_row("Average File Size", self.format_file_size(int(summary_stats['average_file_size'])))
        table.add_row("Average Lines/File", f"{summary_stats['average_lines_per_file']:.1f}")
        
        return table
    
    def _create_file_types_table(self, result: AnalysisResult) -> Table:
        """Create file types breakdown table"""
        breakdown = self.get_file_type_breakdown(result)
        
        table = Table(title="📁 File Types Breakdown", box=box.ROUNDED)
        table.add_column("File Type", style="cyan", width=15)
        table.add_column("Count", style="green", width=8)
        table.add_column("Lines", style="yellow", width=12)
        table.add_column("Size (MB)", style="magenta", width=12)
        table.add_column("Percentage", style="blue", width=12)
        
        # Sort by count descending
        sorted_types = sorted(breakdown.items(), key=lambda x: x[1]['count'], reverse=True)
        
        for file_type, data in sorted_types:
            table.add_row(
                file_type,
                str(data['count']),
                self.format_number(data['lines']),
                f"{data['size_mb']:.2f}",
                f"{data['percentage']:.1f}%"
            )
        
        return table
    
    def _create_largest_files_table(self, result: AnalysisResult) -> Table:
        """Create largest files table"""
        largest_files = self.get_largest_files(result, 10)
        
        table = Table(title="📏 Largest Files", box=box.ROUNDED)
        table.add_column("File", style="cyan", width=25)
        table.add_column("Type", style="green", width=12)
        table.add_column("Size", style="yellow", width=12)
        table.add_column("Lines", style="magenta", width=8)
        table.add_column("Code/Comm/Blank", style="blue", width=15)
        
        for file_info in largest_files:
            code_comm_blank = f"{file_info.code_lines}/{file_info.comment_lines}/{file_info.blank_lines}"
            table.add_row(
                file_info.name,
                file_info.type,
                self.format_file_size(file_info.size),
                str(file_info.lines),
                code_comm_blank
            )
        
        return table
    
    def _create_detailed_metrics_table(self, result: AnalysisResult) -> Table:
        """Create detailed metrics table"""
        detailed_metrics = self.get_detailed_metrics(result)
        
        table = Table(title="🔍 Detailed Metrics", box=box.ROUNDED)
        table.add_column("File Type", style="cyan", width=15)
        table.add_column("Code Lines", style="green", width=12)
        table.add_column("Comment Lines", style="yellow", width=15)
        table.add_column("Blank Lines", style="magenta", width=12)
        table.add_column("Comment Ratio", style="blue", width=15)
        table.add_column("Files", style="red", width=8)
        
        # Sort by code lines descending
        sorted_metrics = sorted(detailed_metrics.items(), key=lambda x: x[1]['code_lines'], reverse=True)
        
        for file_type, metrics in sorted_metrics:
            table.add_row(
                file_type,
                self.format_number(metrics['code_lines']),
                self.format_number(metrics['comment_lines']),
                self.format_number(metrics['blank_lines']),
                f"{metrics['comment_ratio']:.1f}%",
                str(metrics['file_count'])
            )
        
        return table
    
    def _create_project_tree(self, result: AnalysisResult, max_depth: int = 3) -> Tree:
        """Create project structure tree with file statistics"""
        from pathlib import Path
        
        project_path = Path(result.project_path)
        
        def create_tree_node(path: Path, current_depth: int = 0) -> Tree:
            if current_depth >= max_depth:
                return Tree("...")
            
            # Find file info for this path
            file_info = None
            for file_detail in result.files:
                if Path(file_detail.path) == path:
                    file_info = file_detail
                    break
            
            if path.is_file():
                if file_info:
                    size_str = self.format_file_size(file_info.size)
                    tree = Tree(f"📄 {path.name} ({file_info.type}) - {size_str}, {file_info.lines} lines")
                else:
                    tree = Tree(f"📄 {path.name}")
            else:
                tree = Tree(f"📁 {path.name}")
            
            if current_depth >= max_depth - 1:
                tree.add("...")
                return tree
            
            try:
                items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
                for item in items[:20]:  # Limit to first 20 items
                    if self._should_ignore_item(item, result):
                        continue
                    
                    if item.is_file():
                        # Find file info
                        item_info = None
                        for file_detail in result.files:
                            if Path(file_detail.path) == item:
                                item_info = file_detail
                                break
                        
                        if item_info:
                            size_str = self.format_file_size(item_info.size)
                            tree.add(f"📄 {item.name} ({item_info.type}) - {size_str}, {item_info.lines} lines")
                        else:
                            tree.add(f"📄 {item.name}")
                    
                    elif item.is_dir():
                        subtree = create_tree_node(item, current_depth + 1)
                        if subtree:
                            tree.add(subtree)
                
                if len(list(path.iterdir())) > 20:
                    tree.add("...")
                    
            except (PermissionError, OSError):
                tree.add("❌ Access denied")
            
            return tree
        
        return create_tree_node(project_path)
    
    def _should_ignore_item(self, item: Path, result: AnalysisResult) -> bool:
        """Check if item should be ignored in tree display"""
        # Check if it's in the analysis results
        if item.is_file():
            return not any(Path(f.path) == item for f in result.files)
        return False


# Register the rich reporter
reporter_registry.register('rich', RichReporter)