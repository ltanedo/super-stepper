"""
Test file to demonstrate super_stepper functionality.
"""

import time
from super_stepper import step, print_summary, reset, start_workflow


@step(phase="initialization", task="Setup logging", increment=1.0)
def setup_logging():
    """Setup logging system."""
    time.sleep(0.5)
    return True


@step(phase="initialization", task="Load config file", increment=2.0)
def load_config():
    """Load configuration file."""
    time.sleep(0.8)
    return True


@step(phase="initialization", task="Connect to database", increment=3.0)
def connect_db():
    """Connect to database."""
    time.sleep(1.0)
    return False  # Simulate failure


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
    return False  # Simulate failure


@step(phase="cleanup", task="Archive old files", increment=1.0)
def archive_files():
    """Archive old log files."""
    time.sleep(0.6)
    return True


@step(phase="cleanup", task="Send notifications", increment=2.0)
def send_notifications():
    """Send completion notifications."""
    time.sleep(0.4)
    return True


def main():
    """Run the test workflow."""
    print("Testing super_stepper module...\n")

    # Reset any previous state
    reset()

    # Start the workflow display (this will show all registered tasks)
    start_workflow()

    # Execute tasks in phase order: initialization -> data_processing -> cleanup

    # Phase 1: Initialization (in increment order)
    setup_logging()      # increment 1.0
    load_config()        # increment 2.0
    connect_db()         # increment 3.0

    # Phase 2: Data Processing (in increment order)
    fetch_users()        # increment 1.0
    process_transactions() # increment 2.0
    generate_reports()   # increment 3.0

    # Phase 3: Cleanup (in increment order)
    archive_files()      # increment 1.0
    send_notifications() # increment 2.0

    # Print final summary
    print_summary()


if __name__ == "__main__":
    main()
