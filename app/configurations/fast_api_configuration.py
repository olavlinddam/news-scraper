import signal
import sys

import uvicorn
import logging
from fastapi import FastAPI

from app.features.news.news_router import news_router
from app.features.news.webdriver_manager import webdriver_manager


def configure_fast_api():
    logger = logging.getLogger(__name__)

    #  Define the FastAPI app
    app = FastAPI(debug=True)

    @app.on_event("shutdown")
    def shutdown_event():
        for driver in webdriver_manager().open_drivers:
            webdriver_manager().dispose_driver(driver)
        logger.fatal("Application shutdown")

    # app = FastAPI(dependencies=[Depends(get_query_token)], debug=True)

    app.include_router(news_router)
    return app  # Return the FastAPI app instance

# def signal_handler(sig, frame):
#     print("Caught signal, shutting down...")
#     shutdown_event() # Call your shutdown event function
#     sys.exit(0)
#
# # Set up signal handlers
# signal.signal(signal.SIGINT, signal_handler)
# signal.signal(signal.SIGTERM, signal_handler)
