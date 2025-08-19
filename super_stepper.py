"""
super_stepper - A Python decorator module for creating beautiful, organized workflow displays.

This module provides a decorator that groups tasks by phase and sorts them by increment,
displaying progress with spinning wheels that turn into checkmarks or X marks based on success/failure.

Features:
- Phase-based task organization in execution order
- Automatic task sorting by increment within phases
- Enhanced error handling with custom messages and exception capture
- Flexible return formats (boolean or tuple)
- Live progress display with animated spinners
- Comprehensive failure reporting with detailed error messages
- Out-of-order execution support with logical display organization

Example:
    from super_stepper import step, print_summary, reset, start_workflow

    @step(phase="setup", task="Initialize", increment=1.0)
    def init():
        return True

    @step(phase="setup", task="Configure", increment=2.0)
    def configure():
        return False, "Config file missing"

    reset()
    start_workflow()
    init()
    configure()
    print_summary()
"""

import time
import threading
from typing import Dict, List, Tuple, Callable, Any
from functools import wraps
from rich.console import Console
from rich.text import Text
from rich.live import Live

# Global storage for tasks and results
_tasks: Dict[str, List[Tuple[float, str, Callable, bool, bool, str]]] = {}  # phase -> [(increment, task, func, completed, success, error_message)]
_failed_tasks: List[Tuple[str, str, str]] = []  # [(phase, task, error_message)]
_phase_order: List[str] = []  # Track the order phases are encountered
_console = Console()
_live_display = None
_current_task = None
_spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
_spinner_index = 0
_display_started = False


def step(phase: str, task: str, increment: float):
    """
    Decorator for stepped actions that groups tasks by phase and sorts by increment.

    Args:
        phase (str): The phase name to group tasks under
        task (str): The task description
        increment (float): The sort order within the phase

    Returns:
        bool: True if the task succeeded, False if it failed
    """
    def decorator(func: Callable) -> Callable:
        # Register the task when decorator is applied
        if phase not in _tasks:
            _tasks[phase] = []
            # Track phase order
            if phase not in _phase_order:
                _phase_order.append(phase)

        # Check if task already exists to avoid duplicates
        task_exists = False
        for inc, tsk, f, completed, success, error_msg in _tasks[phase]:
            if inc == increment and tsk == task and f == func:
                task_exists = True
                break

        if not task_exists:
            _tasks[phase].append((increment, task, func, False, False, ""))

        @wraps(func)
        def wrapper(*args, **kwargs):
            global _current_task, _display_started

            # Ensure phase exists
            if phase not in _tasks:
                _tasks[phase] = []
                # Also ensure phase order is maintained
                if phase not in _phase_order:
                    _phase_order.append(phase)

            # Find this task in the registry
            task_entry = None
            for i, (inc, tsk, f, completed, success, error_msg) in enumerate(_tasks[phase]):
                if inc == increment and tsk == task and f == func:
                    task_entry = i
                    break

            if task_entry is None:
                # This shouldn't happen, but add as fallback
                _tasks[phase].append((increment, task, func, False, False, ""))
                task_entry = len(_tasks[phase]) - 1

            # Start live display if not already started
            if not _display_started:
                _start_live_display()
                _display_started = True

            # Set current task for spinner
            _current_task = (phase, task)

            try:
                # Execute the function
                result = func(*args, **kwargs)

                # Handle different return formats
                if isinstance(result, tuple) and len(result) == 2:
                    # Tuple return: (success, error_message)
                    success, error_message = result
                    success = bool(success)
                    error_message = str(error_message) if error_message else ""
                else:
                    # Single return: just success boolean
                    success = bool(result)
                    error_message = ""

                # Update task status
                _tasks[phase][task_entry] = (increment, task, func, True, success, error_message)

                # Track failed tasks
                if not success:
                    _failed_tasks.append((phase, task, error_message))

                # Clear current task since it's completed
                _current_task = None

                # Give the background thread time to update the display
                time.sleep(0.2)

                return success

            except Exception as e:
                # Capture exception message as error
                error_message = str(e)

                # Update task status as failed
                _tasks[phase][task_entry] = (increment, task, func, True, False, error_message)
                _failed_tasks.append((phase, task, error_message))

                # Clear current task since it's completed
                _current_task = None

                # Give the background thread time to update the display
                time.sleep(0.2)

                return False

        return wrapper
    return decorator


def _start_live_display():
    """Start the live display showing all tasks."""
    global _live_display

    def update_spinner():
        global _spinner_index
        while _live_display and _live_display.is_started:
            _spinner_index = (_spinner_index + 1) % len(_spinner_chars)
            if _live_display:
                _live_display.update(_generate_display())
            time.sleep(0.1)

    _live_display = Live(_generate_display(), console=_console, refresh_per_second=10)
    _live_display.start()

    # Start spinner animation in background thread
    spinner_thread = threading.Thread(target=update_spinner, daemon=True)
    spinner_thread.start()


def _generate_display():
    """Generate the current display showing all tasks with their status."""
    display = Text()

    # Use phase order as encountered (same as print_summary)
    for phase in _phase_order:
        if not _tasks[phase]:
            continue

        # Print phase header
        phase_text = Text()
        phase_text.append(f"{phase.upper()}", style="bold cyan")
        display.append(phase_text)
        display.append("\n")

        # Sort tasks by increment
        sorted_tasks = sorted(_tasks[phase], key=lambda x: x[0])

        for increment, task_name, func, completed, success, error_msg in sorted_tasks:
            if completed:
                # Task is completed - show checkmark or X
                if success:
                    display.append("  ✓ ", style="green")
                else:
                    display.append("  ✗ ", style="red")
                display.append(f"{task_name}", style="white")
            elif _current_task and _current_task[0] == phase and _current_task[1] == task_name:
                # Show spinner for current task
                spinner_char = _spinner_chars[_spinner_index]
                display.append(f"  {spinner_char} ", style="yellow")
                display.append(f"{task_name}", style="yellow")
            else:
                # Task not started yet
                display.append("  - ", style="dim white")
                display.append(f"{task_name}", style="dim white")
            display.append("\n")

        display.append("\n")

    return display


def _stop_live_display():
    """Stop the live display."""
    global _live_display
    if _live_display:
        _live_display.stop()
        _live_display = None


def print_summary():
    """Print a summary with completion statistics and failed tasks."""
    # Stop the live display first
    _stop_live_display()

    # Calculate statistics
    total_tasks = 0
    completed_tasks = 0
    failed_tasks = 0

    for phase in _phase_order:
        if not _tasks[phase]:
            continue
        for increment, task_name, func, completed, success, error_msg in _tasks[phase]:
            total_tasks += 1
            if completed:
                completed_tasks += 1
                if not success:
                    failed_tasks += 1

    # Print summary header in same style as phase headers
    summary_header = Text()
    # summary_header.append("SUMMARY", style="bold cyan")
    # _console.print(summary_header)

    # Print single status line with consistent indentation
    if total_tasks > 0:
        if failed_tasks > 0:
            # Some tasks failed
            status_text = Text()
            # status_text.append("", style="white")  # Match task indentation
            status_text.append(f"{failed_tasks} of {total_tasks} tasks failed  ", style="white")
            # status_text.append("✗", style="red")
            _console.print(status_text)

            # List failed tasks with consistent indentation
            for i, (phase, task, error_msg) in enumerate(_failed_tasks, 1):
                failed_text = Text()
                failed_text.append(f"  {i}. ", style="white")
                failed_text.append(f"{phase}: ", style="cyan")
                failed_text.append(f"{task}", style="white")

                # Add error message if available
                if error_msg:
                    failed_text.append(f" - {error_msg}", style="dim white")

                failed_text.append("  ✗", style="red")
                _console.print(failed_text)
        else:
            # All tasks completed successfully
            status_text = Text()
            # status_text.append("  ", style="white")  # Match task indentation
            status_text.append(f"{total_tasks} of {total_tasks} tasks completed  ", style="white")
            status_text.append("✓", style="green")
            _console.print(status_text)
    else:
        status_text = Text()
        status_text.append("  No tasks found", style="dim white")
        _console.print(status_text)

    _console.print()

def start_workflow():
    """Start the workflow by displaying all registered tasks."""
    global _display_started
    if not _display_started and _tasks:
        _start_live_display()
        _display_started = True


def reset():
    """Reset all tasks and failed task tracking."""
    global _tasks, _failed_tasks, _phase_order

    # Clear all data
    _tasks.clear()
    _failed_tasks.clear()
    _phase_order.clear()
