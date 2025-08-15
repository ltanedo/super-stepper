#!/usr/bin/env python3
"""
Typer + Rich CLI Example
Modern Python CLI with type hints and rich terminal output
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text
from typing import Optional
import time

# Initialize Rich console and Typer app
console = Console()
app = typer.Typer(help="Modern CLI deployment tool with rich output")

@app.command()
def deploy(
    environment: str = typer.Argument("staging", help="Environment to deploy to"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be deployed"),
    service: Optional[str] = typer.Option(None, "--service", "-s", help="Specific service to deploy")
):
    """Deploy application to specified environment"""
    
    # Header
    title = Text("🚀 Deployment Manager", style="bold cyan")
    console.print(Panel(title, expand=False))
    
    # Show deployment info
    info_table = Table(show_header=False, box=None)
    info_table.add_row("Environment:", f"[yellow]{environment}[/yellow]")
    info_table.add_row("Service:", f"[cyan]{service or 'all services'}[/cyan]")
    info_table.add_row("Mode:", f"[red]DRY RUN[/red]" if dry_run else "[green]LIVE[/green]")
    console.print(info_table)
    console.print()
    
    if dry_run:
        console.print("[yellow]⚠️  DRY RUN MODE - No actual deployment will occur[/yellow]")
        console.print()
    
    # Deployment steps
    steps = [
        "Validating configuration",
        "Building application",
        "Running tests",
        "Creating deployment package",
        "Uploading to cloud",
        "Updating infrastructure",
        "Health check verification"
    ]
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        for step in steps:
            task = progress.add_task(f"{step}...", total=None)
            
            # Simulate work
            time.sleep(0.8)
            
            progress.remove_task(task)
            console.print(f"[green]✓[/green] {step}")
            
            if verbose:
                console.print(f"  [dim]Completed {step.lower()}[/dim]")
    
    # Success message
    console.print()
    success_text = Text("🎉 Deployment completed successfully!", style="bold green")
    console.print(Panel(success_text, style="green"))

@app.command()
def status(
    environment: str = typer.Argument("staging", help="Environment to check"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format")
):
    """Check deployment status"""
    
    if json_output:
        import json
        status_data = {
            "environment": environment,
            "status": "healthy",
            "services": ["api", "web", "worker"],
            "last_deployment": "2024-01-15T10:30:00Z"
        }
        console.print_json(data=status_data)
        return
    
    console.print(f"[bold]Status for [cyan]{environment}[/cyan] environment:[/bold]")
    console.print()
    
    # Status table
    table = Table(title="Service Status")
    table.add_column("Service", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Version", style="yellow")
    table.add_column("Uptime", style="blue")
    
    services = [
        ("api", "healthy", "v1.2.3", "5d 12h"),
        ("web", "healthy", "v1.2.3", "5d 12h"),
        ("worker", "degraded", "v1.2.2", "2d 8h"),
    ]
    
    for service, status, version, uptime in services:
        status_style = "green" if status == "healthy" else "yellow"
        table.add_row(service, f"[{status_style}]{status}[/{status_style}]", version, uptime)
    
    console.print(table)

@app.command()
def logs(
    service: str = typer.Argument(..., help="Service name to get logs for"),
    lines: int = typer.Option(50, "--lines", "-n", help="Number of lines to show"),
    follow: bool = typer.Option(False, "--follow", "-f", help="Follow log output")
):
    """View service logs"""
    
    console.print(f"[bold]Logs for [cyan]{service}[/cyan] (last {lines} lines):[/bold]")
    console.print()
    
    # Simulate log output
    log_entries = [
        "[2024-01-15 10:30:01] INFO: Application started",
        "[2024-01-15 10:30:02] INFO: Database connection established",
        "[2024-01-15 10:30:03] WARN: High memory usage detected",
        "[2024-01-15 10:30:04] INFO: Processing request /api/users",
        "[2024-01-15 10:30:05] ERROR: Failed to connect to external service",
    ]
    
    for entry in log_entries[-lines:]:
        if "ERROR" in entry:
            console.print(f"[red]{entry}[/red]")
        elif "WARN" in entry:
            console.print(f"[yellow]{entry}[/yellow]")
        else:
            console.print(f"[dim]{entry}[/dim]")
    
    if follow:
        console.print("\n[dim]Following logs... (Ctrl+C to stop)[/dim]")

if __name__ == "__main__":
    app()