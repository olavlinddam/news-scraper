import logging
import os
from datetime import datetime


def configure_logger():
    # Define the log directory and filename
    log_dir = '../logs'
    log_filename = f'{log_dir}/log-{datetime.now().strftime("%Y-%m-%d")}.log'

    # Create the log directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configure the logger
    logging.basicConfig(
        level=logging.INFO,  # Set the logging level
        format='%(asctime)s - %(levelname)s - %(message)s',  # Set the log message format
        handlers=[
            logging.FileHandler(log_filename),  # Use a FileHandler to write logs to a file
            logging.StreamHandler()  # Also log to the console
        ]
    )