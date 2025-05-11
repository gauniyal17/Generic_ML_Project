# logger.py
# -----------------------------------------
# This script sets up logging for a Python application.
# Logging is essential for tracking events, debugging, and maintaining logs of operations or errors.
# It dynamically creates a log file named with the current timestamp and stores logs in a dedicated folder.

import logging  # Built-in module to log messages (info, warning, error, etc.)
import os  # Used for file and directory path operations
from datetime import datetime  # Used to get the current date and time

# Generate a log file name with the current timestamp (e.g., 05_05_25_14_30_01.log)
LOG_FILE = f"{datetime.now().strftime('%m_%d_%y_%H_%M_%S')}.log"

# Construct the path: current directory → "logs" folder → log file
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

# Create the directory if it doesn't exist (no error if it already exists)
os.makedirs(logs_path, exist_ok=True)

# Full path to the log file
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Configure logging:
# - filename: where to save logs
# - format: how each log message should appear
# - level: minimum severity level to log (INFO and above)
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# If this file is run directly, log a message
if __name__ == "__main__":
    logging.info("logging has started")
