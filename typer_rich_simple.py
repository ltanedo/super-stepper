#!/usr/bin/env python3
"""
Simplified Typer + Rich CLI Example
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text
import time

console = Console()
app = typer.Typer(help="Simple CLI deployment tool")

@app.command()
def deploy(
    environment: str = typer.Argument("staging", help="Environment to deploy to"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """Deploy application to specified environment"""
    
    console.print(f"[bold]Deploying to [cyan]{environment}[/cyan][/bold]")
    console.print()
    
    steps = [
        "Validating configuration",
        "Building application", 
        "Running tests",
        "Deploying to server"
    ]
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        for step in steps:
            task = progress.add_task(f"{step}...", total=None)
            time.sleep(1)
            progress.remove_task(task)
            console.print(f"[green]✓[/green] {step}")
    
    console.print()
    console.print("[bold green]Deployment completed successfully![/bold green]")

@app.command()
def status():
    """Check deployment status"""
    
    table = Table(title="Service Status")
    table.add_column("Service", style="cyan")
    table.add_column("Status", style="green")
    
    table.add_row("api", "healthy")
    table.add_row("web", "healthy")
    table.add_row("worker", "degraded")
    
    console.print(table)

if __name__ == "__main__":
    app()