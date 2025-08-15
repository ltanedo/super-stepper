# super_stepper

A Python decorator module for printing stepped actions with phases and tasks. This module provides a clean way to organize and display the progress of multi-step processes with visual feedback.

## Features

- **Phase-based organization**: Groups tasks by phase name
- **Automatic sorting**: Tasks are sorted by increment within each phase
- **Visual feedback**: Shows spinning wheel during execution, then green checkmark (✓) for success or red X (✗) for failure
- **Progress tracking**: Displays real-time progress with animated spinners
- **Failure summary**: Shows a summary of all failed tasks at the end
- **Rich formatting**: Uses the `rich` library for beautiful console output

## Installation

Make sure you have the `rich` library installed:

```bash
pip install rich
```

## Usage

### Basic Example

```python
from super_stepper import step, print_summary, reset

@step(phase="setup", task="Initialize database", increment=1.0)
def init_database():
    # Your function logic here
    return True  # Return True for success, False for failure

@step(phase="setup", task="Load configuration", increment=2.0)
def load_config():
    # Your function logic here
    return True

@step(phase="processing", task="Process data", increment=1.0)
def process_data():
    # Your function logic here
    return False  # This will be marked as failed

# Execute your functions
init_database()
load_config()
process_data()

# Print the final summary
print_summary()
```

### Decorator Parameters

- **phase** (str): The phase name to group tasks under (e.g., "setup", "processing", "cleanup")
- **task** (str): The task description that will be displayed
- **increment** (float): The sort order within the phase (tasks are sorted by this value)

### Functions

#### `@step(phase, task, increment)`
Decorator that wraps your function to provide progress tracking.

#### `print_summary()`
Prints a complete summary of all phases, tasks, and any failures.

#### `reset()`
Clears all task history and failure tracking. Useful when running multiple workflows.

## Output Example

```
  ⠋ Initialize database    # Spinner while running
  ✓ Initialize database    # Success
  ✓ Load configuration
  ✗ Process data          # Failure

PROCESSING
  ✗ Process data

SETUP
  ✓ Initialize database
  ✓ Load configuration

FAILED TASKS
✗ processing: Process data
```

## Advanced Usage

### Multiple Phases with Different Increments

```python
@step(phase="initialization", task="Setup logging", increment=1.0)
def setup_logging():
    return True

@step(phase="initialization", task="Load config", increment=2.0)
def load_config():
    return True

@step(phase="data_processing", task="Fetch data", increment=1.0)
def fetch_data():
    return True

@step(phase="data_processing", task="Transform data", increment=2.0)
def transform_data():
    return True

@step(phase="cleanup", task="Archive logs", increment=1.0)
def archive_logs():
    return True
```

### Error Handling

The decorator automatically handles exceptions in your functions. If an exception occurs, the task will be marked as failed and the exception will be caught (not re-raised).

```python
@step(phase="risky", task="Dangerous operation", increment=1.0)
def dangerous_operation():
    raise Exception("Something went wrong!")
    return True  # This won't be reached

# This will show as failed in the output
dangerous_operation()
```

## Requirements

- Python 3.6+
- rich library

## Notes

- Functions decorated with `@step` should return `True` for success or `False` for failure
- Tasks are displayed in the order they are executed, but the final summary groups them by phase and sorts by increment
- The spinner animation runs in a separate thread and automatically stops when the function completes
- Use `reset()` between different workflows to clear the task history
