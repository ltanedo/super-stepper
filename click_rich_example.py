#!/usr/bin/env python3
"""
Click + Rich CLI Example
Established Python CLI framework with rich terminal output
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.text import Text
from rich.prompt import Confirm
import time

# Initialize Rich console
console = Console()

@click.group()
@click.version_option(version="1.0.0")
@click.pass_context
def cli(ctx):
    """🔧 DevOps CLI Tool - Manage your infrastructure with style"""
    ctx.ensure_object(dict)
    
    # Welcome banner
    banner = Text("DevOps CLI Tool", style="bold magenta")
    console.print(Panel(banner, subtitle="v1.0.0", expand=False))

@cli.command()
@click.argument('project_name')
@click.option('--template', '-t', default='basic', 
              type=click.Choice(['basic', 'web', 'api', 'microservice']),
              help='Project template to use')
@click.option('--language', '-l', default='python',
              type=click.Choice(['python', 'javascript', 'go', 'rust']),
              help='Programming language')
@click.option('--force', is_flag=True, help='Overwrite existing project')
def init(project_name, template, language, force):
    """Initialize a new project"""
    
    console.print(f"[bold]Initializing project: [cyan]{project_name}[/cyan][/bold]")
    console.print(f"Template: [yellow]{template}[/yellow]")
    console.print(f"Language: [green]{language}[/green]")
    console.print()
    
    if not force and click.confirm(f"Create project '{project_name}'?"):
        # Project creation steps
        steps = [
            "Creating project directory",
            "Setting up project structure",
            "Installing dependencies",
            "Configuring development environment",
            "Initializing git repository",
            "Creating initial files"
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("Initializing...", total=len(steps))
            
            for step in steps:
                progress.update(task, description=step)
                time.sleep(0.5)
                progress.advance(task)
                console.print(f"[green]✓[/green] {step}")
        
        console.print()
        success_panel = Panel(
            f"[bold green]🎉 Project '{project_name}' created successfully![/bold green]\n\n"
            f"Next steps:\n"
            f"  cd {project_name}\n"
            f"  ./run.sh",
            title="Success",
            style="green"
        )
        console.print(success_panel)
    else:
        console.print("[yellow]Project creation cancelled[/yellow]")

@cli.command()
@click.option('--environment', '-e', default='development',
              type=click.Choice(['development', 'staging', 'production']),
              help='Environment to build for')
@click.option('--optimize', is_flag=True, help='Enable optimizations')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def build(environment, optimize, verbose):
    """Build the project"""
    
    console.print(f"[bold]Building for [cyan]{environment}[/cyan] environment[/bold]")
    
    if optimize:
        console.print("[yellow]⚡ Optimizations enabled[/yellow]")
    
    console.print()
    
    # Build configuration table
    if verbose:
        config_table = Table(title="Build Configuration")
        config_table.add_column("Setting", style="cyan")
        config_table.add_column("Value", style="yellow")
        
        config_table.add_row("Environment", environment)
        config_table.add_row("Optimization", "enabled" if optimize else "disabled")
        config_table.add_row("Target", "production" if environment == "production" else "development")
        config_table.add_row("Minification", "yes" if optimize else "no")
        
        console.print(config_table)
        console.print()
    
    # Build process
    build_steps = [
        ("Cleaning build directory", 1.0),
        ("Compiling source files", 3.0),
        ("Processing assets", 2.0),
        ("Running optimizations", 2.5 if optimize else 0.5),
        ("Generating bundle", 1.5),
        ("Creating manifest", 0.5)
    ]
    
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        for step_name, duration in build_steps:
            task = progress.add_task(step_name, total=100)
            
            # Simulate build progress
            for i in range(100):
                time.sleep(duration / 100)
                progress.update(task, advance=1)
            
            console.print(f"[green]✓[/green] {step_name}")
    
    console.print()
    console.print("[bold green]🏗️  Build completed successfully![/bold green]")

@cli.command()
@click.option('--port', '-p', default=8000, help='Port to run on')
@click.option('--host', '-h', default='localhost', help='Host to bind to')
@click.option('--reload', is_flag=True, help='Enable auto-reload')
def serve(port, host, reload):
    """Start the development server"""
    
    console.print(f"[bold]Starting server on [cyan]http://{host}:{port}[/cyan][/bold]")
    
    if reload:
        console.print("[yellow]🔄 Auto-reload enabled[/yellow]")
    
    console.print()
    
    # Server startup simulation
    startup_steps = [
        "Loading configuration",
        "Initializing database connections",
        "Setting up middleware",
        "Registering routes",
        "Starting HTTP server"
    ]
    
    for step in startup_steps:
        console.print(f"[dim]...[/dim] {step}")
        time.sleep(0.3)
        console.print(f"[green]✓[/green] {step}")
    
    console.print()
    
    # Server info panel
    server_info = Panel(
        f"[bold green]🚀 Server running![/bold green]\n\n"
        f"URL: [link]http://{host}:{port}[/link]\n"
        f"Environment: development\n"
        f"Auto-reload: {'enabled' if reload else 'disabled'}\n\n"
        f"Press [bold]Ctrl+C[/bold] to stop",
        title="Server Status",
        style="green"
    )
    console.print(server_info)
    
    # Simulate server running
    try:
        console.print("\n[dim]Server logs will appear here...[/dim]")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]🛑 Server stopped[/yellow]")

@cli.command()
@click.argument('service_name')
@click.option('--format', '-f', default='table',
              type=click.Choice(['table', 'json', 'yaml']),
              help='Output format')
def info(service_name, format):
    """Get information about a service"""
    
    if format == 'json':
        import json
        service_data = {
            "name": service_name,
            "status": "running",
            "version": "1.2.3",
            "uptime": "5d 12h 30m",
            "memory_usage": "256MB",
            "cpu_usage": "15%"
        }
        console.print_json(data=service_data)
        return
    
    console.print(f"[bold]Service Information: [cyan]{service_name}[/cyan][/bold]")
    console.print()
    
    # Service info table
    info_table = Table(show_header=False, box=None)
    info_table.add_column("Property", style="cyan", width=15)
    info_table.add_column("Value", style="white")
    
    info_table.add_row("Status", "[green]●[/green] Running")
    info_table.add_row("Version", "1.2.3")
    info_table.add_row("Uptime", "5d 12h 30m")
    info_table.add_row("Memory", "256MB / 512MB")
    info_table.add_row("CPU", "15%")
    info_table.add_row("Port", "8080")
    info_table.add_row("Health", "[green]Healthy[/green]")
    
    console.print(info_table)

if __name__ == '__main__':
    cli()