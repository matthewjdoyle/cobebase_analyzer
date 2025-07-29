"""
Main CLI module for the Codebase Analyzer
"""

import sys
import click
from pathlib import Path
from typing import Optional, List

from ..core.analyzer import CodebaseAnalyzer
from ..core.config import Config, load_config, save_config, create_default_config
from ..utils.logger import configure_logging, get_logger

logger = get_logger(__name__)


@click.group()
@click.version_option(version="2.0.0")
@click.option('--config', type=click.Path(exists=True), help='Configuration file path')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--quiet', '-q', is_flag=True, help='Suppress non-essential output')
@click.pass_context
def cli(ctx, config, verbose, quiet):
    """Codebase Analyzer - Comprehensive codebase analysis tool"""
    # Configure logging
    log_level = 'DEBUG' if verbose else 'INFO'
    configure_logging(level=log_level, quiet=quiet)
    
    # Load configuration
    if config:
        ctx.obj = load_config(config)
    else:
        ctx.obj = load_config()
    
    # Ensure context object is available
    ctx.ensure_object(dict)


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--detailed', is_flag=True, help='Include detailed metrics')
@click.option('--export', type=click.Choice(['json', 'csv', 'txt']), help='Export results to file')
@click.option('--output', type=click.Path(), help='Output file path for export')
@click.option('--ignore', multiple=True, help='Ignore patterns (can be used multiple times)')
@click.option('--max-depth', type=int, help='Maximum directory depth to analyze')
@click.option('--max-file-size', type=int, help='Maximum file size in MB')
@click.pass_context
def analyze(ctx, path, detailed, export, output, ignore, max_depth, max_file_size):
    """Analyze a codebase and display comprehensive metrics"""
    try:
        config = ctx.obj
        
        # Override config with CLI options
        if max_depth is not None:
            config.max_depth = max_depth
        if max_file_size is not None:
            config.max_file_size_mb = max_file_size
        
        # Create analyzer
        analyzer = CodebaseAnalyzer(
            project_path=path,
            config=config,
            ignore_patterns=list(ignore) if ignore else None
        )
        
        # Perform analysis
        logger.info(f"Starting analysis of {path}")
        result = analyzer.analyze()
        
        # Display report
        analyzer.display_report(detailed=detailed)
        
        # Export if requested
        if export:
            if output:
                analyzer.export_result(export, output)
            else:
                analyzer.export_result(export)
            logger.info(f"Results exported in {export.upper()} format")
        
        return result
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--max-depth', type=int, default=3, help='Maximum depth to show')
@click.pass_context
def structure(ctx, path, max_depth):
    """Show project structure as a tree"""
    try:
        config = ctx.obj
        
        # Create analyzer
        analyzer = CodebaseAnalyzer(
            project_path=path,
            config=config
        )
        
        # Perform analysis
        result = analyzer.analyze()
        
        # Display structure only
        from ..reporters.rich_reporter import RichReporter
        reporter = RichReporter()
        
        # Create a simplified tree view
        from rich.tree import Tree
        from rich.console import Console
        
        console = Console()
        project_path = Path(path)
        
        def create_tree(path: Path, current_depth: int = 0) -> Tree:
            if current_depth >= max_depth:
                return Tree("...")
            
            tree = Tree(f"📁 {path.name}")
            
            try:
                items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
                for item in items[:20]:  # Limit to first 20 items
                    if item.is_file():
                        tree.add(f"📄 {item.name}")
                    elif item.is_dir():
                        subtree = create_tree(item, current_depth + 1)
                        if subtree:
                            tree.add(subtree)
                
                if len(list(path.iterdir())) > 20:
                    tree.add("...")
                    
            except (PermissionError, OSError):
                tree.add("❌ Access denied")
            
            return tree
        
        tree = create_tree(project_path)
        console.print(tree)
        
    except Exception as e:
        logger.error(f"Structure display failed: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.pass_context
def stats(ctx, path):
    """Quick statistics overview"""
    try:
        config = ctx.obj
        
        # Create analyzer
        analyzer = CodebaseAnalyzer(
            project_path=path,
            config=config
        )
        
        # Perform analysis
        result = analyzer.analyze()
        
        # Display quick stats
        from rich.table import Table
        from rich.console import Console
        from rich import box
        
        console = Console()
        stats = result.stats
        
        table = Table(title="📊 Quick Stats", box=box.ROUNDED)
        table.add_column("Metric", style="cyan", width=15)
        table.add_column("Value", style="green", width=15)
        
        table.add_row("Files", str(stats.total_files))
        table.add_row("Directories", str(stats.total_dirs))
        table.add_row("Lines of Code", f"{stats.total_lines:,}")
        table.add_row("Size", f"{stats.total_size_mb:.2f} MB")
        table.add_row("File Types", str(stats.unique_file_types))
        table.add_row("Analysis Time", f"{result.analysis_duration:.2f}s")
        
        console.print(table)
        
    except Exception as e:
        logger.error(f"Stats display failed: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.pass_context
def interactive(ctx, path):
    """Start interactive exploration mode"""
    try:
        config = ctx.obj
        
        # Create analyzer
        analyzer = CodebaseAnalyzer(
            project_path=path,
            config=config
        )
        
        # Perform analysis
        result = analyzer.analyze()
        
        # Start interactive mode
        from rich.console import Console
        console = Console()
        
        console.print("🎮 Interactive Codebase Explorer")
        console.print("Use the following commands:")
        console.print("  tree - Show project structure")
        console.print("  stats - Show quick statistics")
        console.print("  analyze - Full analysis")
        console.print("  export <format> - Export results")
        console.print("  quit - Exit")
        
        while True:
            try:
                command = input("\n> ").strip().lower()
                
                if command in ['quit', 'exit']:
                    break
                elif command == 'tree':
                    analyzer.display_report(detailed=False)
                elif command == 'stats':
                    from rich.table import Table
                    from rich import box
                    
                    stats = result.stats
                    table = Table(title="📊 Quick Stats", box=box.ROUNDED)
                    table.add_column("Metric", style="cyan")
                    table.add_column("Value", style="green")
                    
                    table.add_row("Files", str(stats.total_files))
                    table.add_row("Directories", str(stats.total_dirs))
                    table.add_row("Lines of Code", f"{stats.total_lines:,}")
                    table.add_row("Size", f"{stats.total_size_mb:.2f} MB")
                    
                    console.print(table)
                elif command == 'analyze':
                    analyzer.display_report(detailed=True)
                elif command.startswith('export '):
                    format_type = command.split()[1]
                    try:
                        analyzer.export_result(format_type)
                        console.print(f"✅ Results exported in {format_type.upper()} format")
                    except Exception as e:
                        console.print(f"❌ Export failed: {e}")
                else:
                    console.print("Unknown command. Type 'quit' to exit.")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                console.print(f"Error: {e}", style="red")
        
    except Exception as e:
        logger.error(f"Interactive mode failed: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--config-file', type=click.Path(), help='Configuration file path')
@click.pass_context
def config(ctx, config_file):
    """Manage configuration"""
    try:
        if config_file:
            config_path = Path(config_file)
            if config_path.exists():
                config = load_config(config_path)
                click.echo(f"Configuration loaded from: {config_path}")
            else:
                config = create_default_config(config_path)
                click.echo(f"Default configuration created at: {config_path}")
        else:
            config = create_default_config()
            click.echo("Default configuration created")
        
        # Display current configuration
        click.echo("\nCurrent Configuration:")
        click.echo(f"  Max File Size: {config.max_file_size_mb} MB")
        click.echo(f"  Max Depth: {config.max_depth or 'Unlimited'}")
        click.echo(f"  Follow Symlinks: {config.follow_symlinks}")
        click.echo(f"  Include Hidden: {config.include_hidden}")
        click.echo(f"  Show Progress: {config.show_progress}")
        click.echo(f"  Color Output: {config.color_output}")
        
    except Exception as e:
        logger.error(f"Configuration management failed: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--format', 'export_format', type=click.Choice(['json', 'csv', 'txt']), 
              default='json', help='Export format')
@click.option('--output', type=click.Path(), help='Output file path')
@click.pass_context
def export(ctx, path, export_format, output):
    """Export analysis results"""
    try:
        config = ctx.obj
        
        # Create analyzer
        analyzer = CodebaseAnalyzer(
            project_path=path,
            config=config
        )
        
        # Perform analysis
        result = analyzer.analyze()
        
        # Export results
        if output:
            analyzer.export_result(export_format, output)
        else:
            analyzer.export_result(export_format)
        
        click.echo(f"✅ Results exported in {export_format.upper()} format")
        
    except Exception as e:
        logger.error(f"Export failed: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def main():
    """Main entry point"""
    cli()


if __name__ == '__main__':
    main()