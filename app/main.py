import signal
import sys
import uvicorn

from app.configurations.fast_api_configuration import configure_fast_api
from app.configurations.logging_configuration import configure_logger
from app.configurations.shutdown_configuration import configure_shutdown_logic

configure_logger()


if __name__ == "__main__":
    configure_logger()
    configure_shutdown_logic()
    app = configure_fast_api()  # Get the FastAPI app instance

    uvicorn.run(app, host="0.0.0.0", port=8000)  # Run the FastAPI app with Uvicorn
