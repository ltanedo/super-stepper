"""
Example usage of the super_stepper decorator module.
"""

import time
import random
from super_stepper import step, print_summary, reset


# Example functions with the step decorator
@step(phase="setup", task="Initialize database", increment=1.0)
def init_database():
    """Simulate database initialization."""
    time.sleep(1)  # Simulate work
    return True  # Success


@step(phase="setup", task="Load configuration", increment=2.0)
def load_config():
    """Simulate configuration loading."""
    time.sleep(0.8)  # Simulate work
    return True  # Success


@step(phase="setup", task="Validate environment", increment=3.0)
def validate_env():
    """Simulate environment validation."""
    time.sleep(0.5)  # Simulate work
    return random.choice([True, False])  # Random success/failure


@step(phase="processing", task="Process data batch 1", increment=1.0)
def process_batch_1():
    """Simulate processing first batch."""
    time.sleep(1.2)  # Simulate work
    return True  # Success


@step(phase="processing", task="Process data batch 2", increment=2.0)
def process_batch_2():
    """Simulate processing second batch."""
    time.sleep(0.9)  # Simulate work
    return random.choice([True, False])  # Random success/failure


@step(phase="processing", task="Validate results", increment=3.0)
def validate_results():
    """Simulate result validation."""
    time.sleep(0.7)  # Simulate work
    return True  # Success


@step(phase="cleanup", task="Archive logs", increment=1.0)
def archive_logs():
    """Simulate log archiving."""
    time.sleep(0.6)  # Simulate work
    return True  # Success


@step(phase="cleanup", task="Clear temporary files", increment=2.0)
def clear_temp_files():
    """Simulate temporary file cleanup."""
    time.sleep(0.4)  # Simulate work
    return random.choice([True, False])  # Random success/failure


def main():
    """Run the example workflow."""
    print("Starting workflow with super_stepper...\n")
    
    # Reset any previous state
    reset()
    
    # Execute tasks in any order - they will be grouped by phase and sorted by increment
    init_database()
    process_batch_1()
    archive_logs()
    load_config()
    process_batch_2()
    clear_temp_files()
    validate_env()
    validate_results()
    
    # Print final summary
    print_summary()


if __name__ == "__main__":
    main()
