"""
CLI command implementations
"""

import sys
import click
from pathlib import Path

# Rich imports for beautiful output
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from core.analyzer import CodebaseAnalyzer
from reports.reporter import Reporter
from reports.visualizer import Visualizer
from utils.file_utils import DEFAULT_IGNORE_PATTERNS


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Codebase Analyzer - Comprehensive codebase analysis tool"""
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--detailed', is_flag=True, help='Include detailed metrics')
@click.option('--visualize', is_flag=True, help='Create matplotlib visualizations')
@click.option('--export', type=click.Choice(['json', 'csv', 'txt']), help='Export results to file')
@click.option('--ignore', multiple=True, help='Ignore patterns (can be used multiple times)')
@click.option('--max-depth', type=int, help='Maximum directory depth to analyze')
@click.option('--sort-by', type=click.Choice(['size', 'lines', 'name']), default='size', help='Sort results by field')
def analyze(path, detailed, visualize, export, ignore, max_depth, sort_by):
    """Analyze a codebase and display comprehensive metrics"""
    try:
        ignore_patterns = list(ignore) if ignore else DEFAULT_IGNORE_PATTERNS
        analyzer = CodebaseAnalyzer(path, ignore_patterns, max_depth)
        
        console = Console() if RICH_AVAILABLE else None
        if console:
            console.print(Panel.fit("🔍 Starting Codebase Analysis", style="bold blue"))
        
        # Perform analysis
        stats = analyzer.analyze()
        
        # Generate and display report
        reporter = Reporter(stats)
        reporter.display_report(detailed)
        
        # Create visualizations if requested
        if visualize:
            try:
                if console:
                    console.print("\n📊 Creating visualizations...", style="bold blue")
                
                visualizer = Visualizer(stats)
                created_files = visualizer.create_all_visualizations(show=False)
                
                if console:
                    console.print(f"✅ Created {len(created_files)} visualizations:", style="green")
                    for file_path in created_files:
                        console.print(f"   📊 {file_path}")
                else:
                    print(f"Created {len(created_files)} visualizations:")
                    for file_path in created_files:
                        print(f"  - {file_path}")
                        
            except ImportError:
                error_msg = "Matplotlib is required for visualizations. Install with: pip install matplotlib"
                if console:
                    console.print(error_msg, style="red")
                else:
                    print(f"Error: {error_msg}")
            except Exception as e:
                error_msg = f"Failed to create visualizations: {e}"
                if console:
                    console.print(error_msg, style="red")
                else:
                    print(f"Error: {error_msg}")
        
        # Export if requested
        if export:
            reporter.export_results(export)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--max-depth', type=int, default=3, help='Maximum depth to show')
def structure(path, max_depth):
    """Show project structure as a tree"""
    if not RICH_AVAILABLE:
        click.echo("Rich library is required for tree visualization. Install with: pip install rich")
        return
    
    try:
        analyzer = CodebaseAnalyzer(path)
        stats = analyzer.analyze()
        
        reporter = Reporter(stats)
        tree = reporter._create_project_tree_with_stats(max_depth)
        
        console = Console()
        console.print(tree)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--visualize', is_flag=True, help='Create visualizations for quick stats')
def stats(path, visualize):
    """Quick statistics overview"""
    try:
        analyzer = CodebaseAnalyzer(path)
        stats = analyzer.analyze()
        
        console = Console() if RICH_AVAILABLE else None
        if console:
            summary_table = Table(title="📊 Quick Stats", box=box.ROUNDED)
            summary_table.add_column("Metric", style="cyan", width=15)
            summary_table.add_column("Value", style="green", width=15)
            
            summary_table.add_row("Files", str(stats['total_files']))
            summary_table.add_row("Directories", str(stats['total_dirs']))
            summary_table.add_row("Lines of Code", f"{stats['total_lines']:,}")
            summary_table.add_row("Size", f"{stats['total_size'] / (1024*1024):.2f} MB")
            summary_table.add_row("File Types", str(len(stats['file_types'])))
            
            console.print(summary_table)
        else:
            print(f"Files: {stats['total_files']}")
            print(f"Directories: {stats['total_dirs']}")
            print(f"Lines of Code: {stats['total_lines']:,}")
            print(f"Size: {stats['total_size'] / (1024*1024):.2f} MB")
            print(f"File Types: {len(stats['file_types'])}")
        
        # Create visualizations if requested
        if visualize:
            try:
                if console:
                    console.print("\n📊 Creating quick visualizations...", style="bold blue")
                
                visualizer = Visualizer(stats)
                # Create just a few key visualizations for quick stats
                created_files = []
                
                # File types pie chart
                pie_chart = visualizer.create_file_types_pie_chart(
                    save_path="quick_stats_file_types.png", show=False)
                if pie_chart:
                    created_files.append(pie_chart)
                
                # Lines by type bar chart
                bar_chart = visualizer.create_lines_by_type_bar_chart(
                    save_path="quick_stats_lines_by_type.png", show=False)
                if bar_chart:
                    created_files.append(bar_chart)
                
                if console:
                    console.print(f"✅ Created {len(created_files)} quick visualizations:", style="green")
                    for file_path in created_files:
                        console.print(f"   📊 {file_path}")
                else:
                    print(f"Created {len(created_files)} quick visualizations:")
                    for file_path in created_files:
                        print(f"  - {file_path}")
                        
            except ImportError:
                error_msg = "Matplotlib is required for visualizations. Install with: pip install matplotlib"
                if console:
                    console.print(error_msg, style="red")
                else:
                    print(f"Error: {error_msg}")
            except Exception as e:
                error_msg = f"Failed to create visualizations: {e}"
                if console:
                    console.print(error_msg, style="red")
                else:
                    print(f"Error: {error_msg}")
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('path', type=click.Path(exists=True))
def interactive(path):
    """Start interactive exploration mode"""
    if not RICH_AVAILABLE:
        click.echo("Rich library is required for interactive mode. Install with: pip install rich")
        return
    
    console = Console()
    console.print(Panel.fit("🎮 Interactive Codebase Explorer", style="bold green"))
    console.print("Use the following commands:")
    console.print("  tree - Show project structure")
    console.print("  stats - Show quick statistics")
    console.print("  analyze - Full analysis")
    console.print("  visualize - Create all visualizations")
    console.print("  quit - Exit")
    
    analyzer = CodebaseAnalyzer(path)
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == 'quit' or command == 'exit':
                break
            elif command == 'tree':
                stats = analyzer.analyze()
                reporter = Reporter(stats)
                tree = reporter._create_project_tree_with_stats()
                console.print(tree)
            elif command == 'stats':
                stats = analyzer.analyze()
                summary_table = Table(title="📊 Quick Stats", box=box.ROUNDED)
                summary_table.add_column("Metric", style="cyan")
                summary_table.add_column("Value", style="green")
                
                summary_table.add_row("Files", str(stats['total_files']))
                summary_table.add_row("Directories", str(stats['total_dirs']))
                summary_table.add_row("Lines of Code", f"{stats['total_lines']:,}")
                summary_table.add_row("Size", f"{stats['total_size'] / (1024*1024):.2f} MB")
                
                console.print(summary_table)
            elif command == 'analyze':
                stats = analyzer.analyze()
                reporter = Reporter(stats)
                reporter.display_report(detailed=True)
            elif command == 'visualize':
                try:
                    stats = analyzer.analyze()
                    console.print("📊 Creating visualizations...", style="bold blue")
                    visualizer = Visualizer(stats)
                    created_files = visualizer.create_all_visualizations(show=False)
                    console.print(f"✅ Created {len(created_files)} visualizations:", style="green")
                    for file_path in created_files:
                        console.print(f"   📊 {file_path}")
                except ImportError:
                    console.print("Matplotlib is required for visualizations. Install with: pip install matplotlib", style="red")
                except Exception as e:
                    console.print(f"Failed to create visualizations: {e}", style="red")
            else:
                console.print("Unknown command. Available: tree, stats, analyze, visualize, quit", style="yellow")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"Error: {e}", style="red")


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--output-dir', default='visualizations', help='Output directory for visualizations')
@click.option('--show', is_flag=True, help='Show visualizations in addition to saving them')
def visualize(path, output_dir, show):
    """Create beautiful matplotlib visualizations of codebase statistics"""
    try:
        console = Console() if RICH_AVAILABLE else None
        if console:
            console.print(Panel.fit("📊 Creating Codebase Visualizations", style="bold blue"))
        
        # Analyze codebase
        analyzer = CodebaseAnalyzer(path)
        stats = analyzer.analyze()
        
        # Create visualizations
        try:
            visualizer = Visualizer(stats)
            created_files = visualizer.create_all_visualizations(output_dir=output_dir, show=show)
            
            if console:
                console.print(f"✅ Successfully created {len(created_files)} visualizations in '{output_dir}':", style="green")
                for file_path in created_files:
                    console.print(f"   📊 {file_path}")
                console.print(f"\n🎨 Visualizations include:", style="bold blue")
                console.print("   • File types distribution (pie chart)")
                console.print("   • Lines of code by file type (bar chart)")
                console.print("   • File size distribution (bar chart)")
                console.print("   • Largest files (horizontal bar chart)")
                console.print("   • Code composition metrics (stacked bar chart)")
            else:
                print(f"Successfully created {len(created_files)} visualizations in '{output_dir}':")
                for file_path in created_files:
                    print(f"  - {file_path}")
                    
        except ImportError:
            error_msg = "Matplotlib is required for visualizations. Install with: pip install matplotlib"
            if console:
                console.print(error_msg, style="red")
            else:
                print(f"Error: {error_msg}")
        except Exception as e:
            error_msg = f"Failed to create visualizations: {e}"
            if console:
                console.print(error_msg, style="red")
            else:
                print(f"Error: {error_msg}")
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def main():
    """Main entry point"""
    cli()


if __name__ == '__main__':
    main()