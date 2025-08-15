#!/usr/bin/env python3
"""
Single Command Typer + Rich Example
Runs directly without requiring subcommands
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
import time

console = Console()

def main(
    environment: str = typer.Argument("staging", help="Environment to deploy to"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    action: str = typer.Option("deploy", "--action", "-a", help="Action to perform: deploy, status, or logs")
):
    """Simple deployment tool with rich output"""
    
    if action == "deploy":
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
                time.sleep(0.8)
                progress.remove_task(task)
                console.print(f"[green]✓[/green] {step}")
                
                if verbose:
                    console.print(f"  [dim]Completed {step.lower()}[/dim]")
        
        console.print()
        success_text = "Deployment completed successfully!"
        console.print(Panel(success_text, style="green"))
    
    elif action == "status":
        console.print(f"[bold]Status for [cyan]{environment}[/cyan] environment:[/bold]")
        console.print()
        
        table = Table(title="Service Status")
        table.add_column("Service", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Version", style="yellow")
        
        services = [
            ("api", "healthy", "v1.2.3"),
            ("web", "healthy", "v1.2.3"),
            ("worker", "degraded", "v1.2.2"),
        ]
        
        for service, status, version in services:
            status_style = "green" if status == "healthy" else "yellow"
            table.add_row(service, f"[{status_style}]{status}[/{status_style}]", version)
        
        console.print(table)
    
    elif action == "logs":
        console.print(f"[bold]Recent logs for [cyan]{environment}[/cyan]:[/bold]")
        console.print()
        
        log_entries = [
            "[2024-01-15 10:30:01] INFO: Application started",
            "[2024-01-15 10:30:02] INFO: Database connection established", 
            "[2024-01-15 10:30:03] WARN: High memory usage detected",
            "[2024-01-15 10:30:04] INFO: Processing request /api/users",
            "[2024-01-15 10:30:05] ERROR: Failed to connect to external service",
        ]
        
        for entry in log_entries:
            if "ERROR" in entry:
                console.print(f"[red]{entry}[/red]")
            elif "WARN" in entry:
                console.print(f"[yellow]{entry}[/yellow]")
            else:
                console.print(f"[dim]{entry}[/dim]")

if __name__ == "__main__":
    typer.run(main)