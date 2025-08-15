from rich.console import Console
from rich.text import Text
import time

console = Console()

def print_job_header(job_name, duration, job_id):
    """Print a job header with checkmark, name, duration and ID"""
    header = Text()
    header.append("✓ ", style="green")
    header.append(f"{job_name} ", style="cyan")
    header.append("in ", style="white")
    header.append(f"{duration} ", style="yellow")
    header.append("(ID ", style="white")
    header.append(f"{job_id}", style="cyan")
    header.append(")", style="white")
    console.print(header)

def print_step(step_name, completed=True):
    """Print a job step with checkmark or dash"""
    step = Text()
    if completed:
        step.append("  ✓ ", style="green")
    else:
        step.append("  - ", style="white")
    step.append(step_name, style="white")
    console.print(step)

# Main output
console.print(Text("JOBS", style="bold cyan"))
console.print()

# Build-deb job
print_job_header("build-deb", "1m46s", "48178950323")
print_step("Set up job")
print_step("Run actions/checkout@v4")
print_step("Install build dependencies")
print_step("Build Debian package")
print_step("Upload Debian package")
print_step("Post Run actions/checkout@v4")
print_step("Complete job")

# Build-windows job
print_job_header("build-windows", "17s", "48178950397")
print_step("Set up job")
print_step("Run actions/checkout@v4")
print_step("Create Windows installer structure")
print_step("Create portable ZIP")
print_step("Upload Windows package")
print_step("Post Run actions/checkout@v4")
print_step("Complete job")

# Create-release job
print_job_header("create-release", "14s", "48179062539")
print_step("Set up job")
print_step("Run actions/checkout@v4")
print_step("Download all artifacts")
print_step("Debug artifacts and files")
print_step("Set release tag")
print_step("Check and delete existing release")
print_step("Create Release")
print_step("Debug release creation", completed=False)
print_step("Post Run actions/checkout@v4")
print_step("Complete job")