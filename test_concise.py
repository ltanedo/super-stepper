"""
Test the new concise error summary format.
"""

import time
from super_stepper import step, summary


@step(phase="setup", task="Init system", increment=1.0)
def init():
    time.sleep(0.1)
    return False, "Init failed"


@step(phase="setup", task="Load config", increment=2.0)
def load_config():
    time.sleep(0.1)
    return False, "Config missing"


@step(phase="setup", task="Start services", increment=3.0)
def start_services():
    time.sleep(0.1)
    return True


@step(phase="processing", task="Connect DB", increment=1.0)
def connect_db():
    time.sleep(0.1)
    return False, "Connection failed"


@step(phase="processing", task="Process data", increment=2.0)
def process_data():
    time.sleep(0.1)
    return True


@step(phase="cleanup", task="Archive", increment=1.0)
def archive():
    time.sleep(0.1)
    return True


def main():
    print("🎯 Testing concise error summary...\n")
    
    init()
    load_config()
    start_services()
    connect_db()
    process_data()
    archive()
    
    summary()


if __name__ == "__main__":
    main()
