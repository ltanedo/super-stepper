# state.py
"""
Shared state module for super_stepper workflow example.
Demonstrates how tasks can modify shared variables across phases.
"""

class AppState:
    def __init__(self):
        # Configuration state
        self.config = {
            "database_url": None,
            "api_key": None,
            "log_level": "INFO",
            "max_connections": 10
        }

        # Database connection state
        self.database = {
            "connection": None,
            "is_connected": False,
            "connection_time": None,
            "last_error": None
        }

        # Data processing state
        self.processing = {
            "users_fetched": 0,
            "transactions_processed": 0,
            "reports_generated": [],
            "processing_start_time": None,
            "processing_end_time": None
        }

        # Cleanup and notification state
        self.cleanup = {
            "files_archived": 0,
            "archive_path": None,
            "notifications_sent": [],
            "cleanup_errors": []
        }

        # Overall workflow state
        self.workflow = {
            "start_time": None,
            "end_time": None,
            "phases_completed": [],
            "overall_success": False
        }

        # Legacy fields for compatibility
        self.cache = {}
        self.user = None

    def reset(self):
        """Reset all state to initial values."""
        self.__init__()

    def get_summary(self):
        """Return a summary of current state."""
        return {
            "config_loaded": self.config["database_url"] is not None,
            "database_connected": self.database["is_connected"],
            "users_processed": self.processing["users_fetched"],
            "transactions_processed": self.processing["transactions_processed"],
            "files_archived": self.cleanup["files_archived"],
            "notifications_sent": len(self.cleanup["notifications_sent"]),
            "phases_completed": len(self.workflow["phases_completed"])
        }

# Global state instance
state = AppState()