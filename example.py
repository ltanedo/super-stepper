"""
Test file demonstrating super_stepper functionality.

This file showcases:
- Basic task decoration with phases and increments
- Different return formats (boolean vs tuple)
- Error handling with custom messages
- Exception handling
- Out-of-order task execution
"""

import time
from super_stepper import step, print_summary, reset, start_workflow


# =============================================================================
# INITIALIZATION PHASE TASKS
# =============================================================================

@step(phase="initialization", task="Setup logging", increment=1.0)
def setup_logging():
    """Setup logging system."""
    time.sleep(0.5)
    return True  # Simple boolean return (backward compatibility)


@step(phase="initialization", task="Load config file", increment=2.0)
def load_config():
    """Load configuration file."""
    time.sleep(0.8)
    return True


@step(phase="initialization", task="Connect to database", increment=3.0)
def connect_db():
    """Connect to database."""
    time.sleep(1.0)
    # Tuple return with custom error message
    return False, "Connection timeout after 30 seconds"


# =============================================================================
# DATA PROCESSING PHASE TASKS
# =============================================================================

@step(phase="data_processing", task="Fetch user data", increment=1.0)
def fetch_users():
    """Fetch user data from API."""
    time.sleep(0.7)
    return True


@step(phase="data_processing", task="Process transactions", increment=2.0)
def process_transactions():
    """Process transaction data."""
    time.sleep(1.2)
    return True


@step(phase="data_processing", task="Generate reports", increment=3.0)
def generate_reports():
    """Generate summary reports."""
    time.sleep(0.9)
    # Tuple return with custom error message
    return False, "Insufficient data for report generation"


# =============================================================================
# CLEANUP PHASE TASKS
# =============================================================================

@step(phase="cleanup", task="Archive old files", increment=1.0)
def archive_files():
    """Archive old log files."""
    time.sleep(0.6)
    # Exception handling demonstration
    raise FileNotFoundError("Archive directory not found: /var/logs/archive")


@step(phase="cleanup", task="Send notifications", increment=2.0)
def send_notifications():
    """Send completion notifications."""
    time.sleep(0.4)
    return True


# =============================================================================
# MAIN WORKFLOW EXECUTION
# =============================================================================

def main():
    """
    Run the test workflow demonstrating super_stepper features.

    This function executes tasks in a deliberately mixed order to showcase:
    - Phase grouping (tasks are grouped by phase regardless of execution order)
    - Increment sorting (tasks within phases are sorted by increment)
    - Error handling (custom messages and exceptions)
    - Live display updates
    - Summary reporting
    """
    print("🚀 Testing super_stepper module...\n")

    # Reset any previous state
    reset()

    # Start the workflow display (shows all registered tasks)
    start_workflow()

    # Execute tasks OUT OF ORDER to demonstrate phase grouping
    print("📋 Executing tasks in mixed order to test phase organization...\n")

    # Deliberately mixed execution order
    archive_files()         # cleanup phase, increment 1.0
    process_transactions()  # data_processing phase, increment 2.0
    setup_logging()         # initialization phase, increment 1.0
    send_notifications()    # cleanup phase, increment 2.0
    connect_db()            # initialization phase, increment 3.0
    fetch_users()           # data_processing phase, increment 1.0
    generate_reports()      # data_processing phase, increment 3.0
    load_config()           # initialization phase, increment 2.0

    # Print final summary with error details
    print_summary()


def demo_simple_workflow():
    """
    Alternative demo showing a simple, ordered workflow.
    Uncomment and call this function for a basic demonstration.
    """
    print("🚀 Simple workflow demo...\n")
    reset()
    start_workflow()

    # Execute in logical order
    setup_logging()
    load_config()
    # connect_db()  # Skip to avoid error

    fetch_users()
    process_transactions()
    # generate_reports()  # Skip to avoid error

    # archive_files()  # Skip to avoid exception
    send_notifications()

    print_summary()


if __name__ == "__main__":
    main()

    # Uncomment to run the simple demo instead:
    # demo_simple_workflow()
