"""
super_stepper - A Python decorator module for printing stepped actions with phases and tasks.

This module provides a decorator that groups tasks by phase and sorts them by increment,
displaying progress with spinning wheels that turn into checkmarks or X marks based on success/failure.
"""

import time
import threading
from typing import Dict, List, Tuple, Callable, Any
from functools import wraps
from rich.console import Console
from rich.text import Text
from rich.live import Live

# Global storage for tasks and results
_tasks: Dict[str, List[Tuple[float, str, Callable, bool, bool]]] = {}  # phase -> [(increment, task, func, completed, success)]
_failed_tasks: List[Tuple[str, str]] = []  # [(phase, task)]
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

        # Check if task already exists to avoid duplicates
        task_exists = False
        for inc, tsk, f, completed, success in _tasks[phase]:
            if inc == increment and tsk == task and f == func:
                task_exists = True
                break

        if not task_exists:
            _tasks[phase].append((increment, task, func, False, False))

        @wraps(func)
        def wrapper(*args, **kwargs):
            global _current_task, _display_started

            # Ensure phase exists
            if phase not in _tasks:
                _tasks[phase] = []

            # Find this task in the registry
            task_entry = None
            for i, (inc, tsk, f, completed, success) in enumerate(_tasks[phase]):
                if inc == increment and tsk == task and f == func:
                    task_entry = i
                    break

            if task_entry is None:
                # This shouldn't happen, but add as fallback
                _tasks[phase].append((increment, task, func, False, False))
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
                success = bool(result)

                # Update task status
                _tasks[phase][task_entry] = (increment, task, func, True, success)

                # Track failed tasks
                if not success:
                    _failed_tasks.append((phase, task))

                return success

            except Exception as e:
                # Update task status as failed
                _tasks[phase][task_entry] = (increment, task, func, True, False)
                _failed_tasks.append((phase, task))

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

    # Sort phases alphabetically
    sorted_phases = sorted(_tasks.keys())

    for phase in sorted_phases:
        if not _tasks[phase]:
            continue

        # Print phase header
        phase_text = Text()
        phase_text.append(f"{phase.upper()}", style="bold cyan")
        display.append(phase_text)
        display.append("\n")

        # Sort tasks by increment
        sorted_tasks = sorted(_tasks[phase], key=lambda x: x[0])

        for increment, task_name, func, completed, success in sorted_tasks:
            if _current_task and _current_task[0] == phase and _current_task[1] == task_name and not completed:
                # Show spinner for current task
                spinner_char = _spinner_chars[_spinner_index]
                display.append(f"  {spinner_char} ", style="yellow")
                display.append(f"{task_name}", style="yellow")
            elif completed:
                if success:
                    display.append("  ✓ ", style="green")
                else:
                    display.append("  ✗ ", style="red")
                display.append(f"{task_name}", style="white")
            else:
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
    """Print a summary of all phases and tasks, including any failures."""
    _console.print()

    # Print all phases and tasks in execution order
    for phase in _phase_order:
        if not _tasks[phase]:
            continue

        # Print phase header
        phase_text = Text()
        phase_text.append(f"{phase.upper()}", style="bold cyan")
        _console.print(phase_text)

        # Sort tasks by increment
        sorted_tasks = sorted(_tasks[phase], key=lambda x: x[0])

        for increment, task_name, func, completed, success in sorted_tasks:
            result = Text()
            if completed:
                if success:
                    result.append("  ✓ ", style="green")
                else:
                    result.append("  ✗ ", style="red")
            else:
                result.append("  - ", style="dim white")
            result.append(f"{task_name}", style="white")
            _console.print(result)

        _console.print()

    # Print failed tasks summary if any
    if _failed_tasks:
        _console.print(Text("FAILED TASKS", style="bold red"))
        for phase, task in _failed_tasks:
            failed_text = Text()
            failed_text.append("✗ ", style="red")
            failed_text.append(f"{phase}: ", style="cyan")
            failed_text.append(f"{task}", style="white")
            _console.print(failed_text)


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
