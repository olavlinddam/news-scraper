import logging
from fastapi import FastAPI

from app.features.news.news_router import news_router
from app.features.subscription.subscription_router import subscription_router

logger = logging.getLogger(__name__)


def configure_fast_api():
    # Define the FastAPI app
    app = FastAPI(debug=True)

    # @app.on_event("shutdown")
    # def shutdown_event_wrapper():
    #     shutdown_event()

    app.include_router(news_router)
    app.include_router(subscription_router)

    return app  # Return the FastAPI app instance
