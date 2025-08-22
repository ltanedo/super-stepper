"""
Test file demonstrating super_stepper.stepper functionality.

This file showcases:
- Basic task decoration with phases and increments
- Different return formats (boolean vs tuple)
- Error handling with custom messages
- Exception handling
- Phase-based workflow organization
"""

import time
import datetime
import super_stepper as stepper
from state import state

# =============================================================================
# INITIALIZATION PHASE TASKS
# =============================================================================
def initialization():
    """Execute all initialization phase tasks."""


    @stepper.step(phase="initialization", task="Setup logging", increment=1.0)
    def setup_logging():
        """Setup logging system."""
        time.sleep(0.5)
        state.config["log_level"] = "DEBUG"
        state.workflow["start_time"] = datetime.datetime.now()
        return True, f"Logging set to {state.config['log_level']}"


    @stepper.step(phase="initialization", task="Load config file", increment=2.0)
    def load_config():
        """Load configuration file."""
        time.sleep(0.8)
        state.config["database_url"] = "postgresql://localhost:5432/mydb"
        state.config["api_key"] = "sk-1234567890abcdef"
        state.config["max_connections"] = 20
        return True, f"Config loaded with {state.config['max_connections']} max connections"


    @stepper.step(phase="initialization", task="Connect to database", increment=3.0)
    def connect_db():
        """Connect to database."""
        time.sleep(1.0)
        if state.config["database_url"]:
            state.database["connection_time"] = datetime.datetime.now()
            state.database["last_error"] = "Connection timeout after 30 seconds"
            return False, state.database["last_error"]
        else:
            return False, "No database URL configured"

    setup_logging()
    load_config()
    connect_db()

# =============================================================================
# DATA PROCESSING PHASE TASKS
# =============================================================================
def data_processing():
    """Execute all data processing phase tasks."""


    @stepper.step(phase="data_processing", task="Fetch user data", increment=1.0)
    def fetch_users():
        """Fetch user data from API."""
        time.sleep(0.7)
        state.processing["users_fetched"] = 1247
        state.processing["processing_start_time"] = datetime.datetime.now()
        return True, f"Fetched {state.processing['users_fetched']} users"


    @stepper.step(phase="data_processing", task="Process transactions", increment=2.0)
    def process_transactions():
        """Process transaction data."""
        time.sleep(1.2)
        # Use data from previous task
        users_count = state.processing["users_fetched"]
        state.processing["transactions_processed"] = users_count * 3  # 3 transactions per user
        return True, f"Processed {state.processing['transactions_processed']} transactions"


    @stepper.step(phase="data_processing", task="Generate reports", increment=3.0)
    def generate_reports():
        """Generate summary reports."""
        time.sleep(0.9)
        # Check if we have enough data
        if state.processing["transactions_processed"] < 1000:
            return False, f"Need 1000+ transactions, only have {state.processing['transactions_processed']}"
        else:
            state.processing["reports_generated"] = ["user_summary.pdf", "transaction_report.xlsx"]
            state.processing["processing_end_time"] = datetime.datetime.now()
            return True, f"Generated {len(state.processing['reports_generated'])} reports"

    fetch_users()
    process_transactions()
    generate_reports()

# =============================================================================
# CLEANUP PHASE TASKS
# =============================================================================
def cleanup():
    """Execute all cleanup phase tasks."""


    @stepper.step(phase="cleanup", task="Archive old files", increment=1.0)
    def archive_files():
        """Archive old log files."""
        time.sleep(0.6)
        # Simulate archiving based on processing results
        if state.processing["transactions_processed"] > 0:
            state.cleanup["files_archived"] = 150
            state.cleanup["archive_path"] = "/var/logs/archive"
            state.cleanup["cleanup_errors"].append("Archive directory not found: /var/logs/archive")
            raise FileNotFoundError("Archive directory not found: /var/logs/archive")
        else:
            return False, "No data to archive"


    @stepper.step(phase="cleanup", task="Send notifications", increment=2.0)
    def send_notifications():
        """Send completion notifications."""
        time.sleep(0.4)
        # Send notifications based on workflow results
        notifications = []
        if state.processing["users_fetched"] > 0:
            notifications.append(f"admin@company.com: Processed {state.processing['users_fetched']} users")
        if len(state.cleanup["cleanup_errors"]) > 0:
            notifications.append(f"ops@company.com: {len(state.cleanup['cleanup_errors'])} cleanup errors")

        state.cleanup["notifications_sent"] = notifications
        state.workflow["end_time"] = datetime.datetime.now()
        state.workflow["phases_completed"] = ["initialization", "data_processing", "cleanup"]

        return True, f"Sent {len(notifications)} notifications"

    archive_files()
    send_notifications()


# =============================================================================
# MAIN WORKFLOW EXECUTION
# =============================================================================
def main():
    """
    Run the test workflow demonstrating super_stepper features with shared state.

    This function executes tasks by calling phase functions in order.
    Each task modifies shared variables in state.py to demonstrate
    how data flows between phases in a workflow.
    """

    # Execute phases in order
    initialization()
    data_processing()
    cleanup()

    # Print final summary with error details
    stepper.summary()


if __name__ == "__main__":
    main()

    # Uncomment to run the simple demo instead:
    # demo_simple_workflow()
