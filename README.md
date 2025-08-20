# 🚀 Super Stepper

A Python decorator module for creating beautiful, organized workflow displays with phases, tasks, and comprehensive error handling.

## ✨ Features

- **Phase Organization**: Group tasks by logical phases that display in execution order
- **Task Sorting**: Tasks within phases are automatically sorted by increment values
- **Live Display**: Real-time progress with animated spinners and status indicators
- **Enhanced Error Handling**: Support for custom error messages and automatic exception capture
- **Flexible Returns**: Functions can return simple booleans or (success, error_message) tuples
- **Beautiful Output**: Rich console formatting with colors and symbols
- **Out-of-Order Execution**: Tasks can be executed in any order but display logically organized

## 🛠️ Installation

```bash
pip install rich
```

## 📖 Quick Start

```python
from super_stepper import step, print_summary, reset, start_workflow
import time

@step(phase="initialization", task="Setup logging", increment=1.0)
def setup_logging():
    time.sleep(0.5)
    return True

@step(phase="initialization", task="Connect to database", increment=2.0)
def connect_db():
    time.sleep(1.0)
    return False, "Connection timeout"  # Custom error message

@step(phase="processing", task="Process data", increment=1.0)
def process_data():
    time.sleep(0.8)
    raise ValueError("Invalid data format")  # Exception handling

# Run workflow
reset()
start_workflow()

setup_logging()
connect_db()
process_data()

print_summary()
```

## 📋 Output Example

```
INITIALIZATION
  ✓ Setup logging
  ✗ Connect to database

PROCESSING
  ✗ Process data

2 of 3 tasks failed
  1. initialization: Connect to database - Connection timeout  ✗
  2. processing: Process data - Invalid data format  ✗
```

## 🎯 Use Cases

- **DevOps Workflows**: Deployment scripts with clear phase organization
- **Data Pipelines**: ETL processes with comprehensive error reporting
- **System Initialization**: Startup sequences with dependency tracking
- **Testing Suites**: Organized test execution with detailed failure reporting

---

# 📚 API Documentation

## Decorator Parameters

- **phase** (str): The phase name to group tasks under (e.g., "setup", "processing", "cleanup")
- **task** (str): The task description that will be displayed
- **increment** (float): The sort order within the phase (tasks are sorted by this value)

## Functions

### `@step(phase, task, increment)`
Decorator that wraps your function to provide progress tracking and error handling.

**Parameters:**
- `phase` (str): Phase name for grouping tasks
- `task` (str): Task description for display
- `increment` (float): Sort order within phase

**Function Return Options:**
- `return True/False` - Simple boolean success/failure
- `return (True/False, "error message")` - Tuple with custom error message
- Exceptions are automatically caught and used as error messages

### `start_workflow()`
Initializes and starts the live display showing all registered tasks.

### `print_summary()`
Prints a comprehensive summary with task counts and detailed error messages.

### `reset()`
Clears all task history and failure tracking. Call before starting a new workflow.

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

### Enhanced Error Handling

The decorator provides comprehensive error handling with multiple options:

#### 1. Simple Boolean Returns (Backward Compatible)
```python
@step(phase="basic", task="Simple task", increment=1.0)
def simple_task():
    return True  # or False
```

#### 2. Tuple Returns with Custom Error Messages
```python
@step(phase="advanced", task="Validation task", increment=1.0)
def validation_task():
    if not validate_data():
        return False, "Data validation failed: missing required fields"
    return True, ""  # Success with empty error message
```

#### 3. Automatic Exception Handling
```python
@step(phase="risky", task="File operation", increment=1.0)
def file_operation():
    # Exception will be caught and used as error message
    raise FileNotFoundError("Config file not found: /etc/myapp.conf")
```

All error messages are displayed in the final summary with detailed information.

## Requirements

- Python 3.6+
- rich library

## Notes

- **Return Formats**: Functions can return `True/False` or `(success, error_message)` tuples
- **Phase Organization**: Tasks are grouped by phase in the order phases are first encountered
- **Task Sorting**: Within each phase, tasks are sorted by increment value
- **Exception Safety**: All exceptions are caught and converted to error messages
- **Live Display**: Spinner animations run in separate threads for real-time feedback
- **Workflow Management**: Use `reset()` between different workflows to clear history
- **Out-of-Order Execution**: Tasks can be called in any order but display logically organized

## Best Practices

1. **Use meaningful phase names**: "initialization", "data_processing", "cleanup"
2. **Set logical increments**: Use 1.0, 2.0, 3.0 for main tasks, 1.1, 1.2 for sub-tasks
3. **Provide helpful error messages**: Use tuple returns for custom error descriptions
4. **Reset between workflows**: Call `reset()` before starting a new workflow
5. **Start workflow display**: Call `start_workflow()` after `reset()` for live updates

## 🧪 Example

Run the example to see all features in action:

```bash
python example.py
```
