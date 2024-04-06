import logging
from datetime import datetime
import os
import uvicorn

from fastapi import FastAPI

from app.configurations.fast_api_configuration import configure_fast_api
from app.configurations.logging_configuration import configure_logger
# from .dependencies import get_query_token
from app.features.news.news_router import news_router
from app.features.news.webdriver_manager import webdriver_manager

# # Define the log directory and filename
# log_dir = '../logs'
# log_filename = f'{log_dir}/log-{datetime.now().strftime("%Y-%m-%d")}.log'
#
# # Create the log directory if it doesn't exist
# if not os.path.exists(log_dir):
#     os.makedirs(log_dir)
#
# # Configure the logger
# logging.basicConfig(
#     level=logging.INFO,  # Set the logging level
#     format='%(asctime)s - %(levelname)s - %(message)s',  # Set the log message format
#     handlers=[
#         logging.FileHandler(log_filename),  # Use a FileHandler to write logs to a file
#         logging.StreamHandler()  # Also log to the console
#     ]
# )

configure_logger()
configure_fast_api()


if __name__ == "__main__":
    configure_logger()
    app = configure_fast_api()  # Get the FastAPI app instance
    uvicorn.run(app, host="0.0.0.0", port=8000) # Run the FastAPI app with Uvicorn
