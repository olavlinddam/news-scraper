import signal
import sys

from app.data.repository import Repository
from app.features.news.webdriver_manager import WebdriverManager
import logging

logger = logging.getLogger(__name__)


def dispose_webdrivers():
    for driver in WebdriverManager().open_drivers:
        WebdriverManager().dispose_driver(driver)


def signal_handler(sig, frame):
    print("Caught signal, shutting down...")
    dispose_webdrivers()
    sys.exit(0)


def configure_shutdown_logic():
    logger.fatal("Application shutdown. Executing shutdown logic.")
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


