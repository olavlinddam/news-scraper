import logging

from selenium import webdriver


class WebdriverManager:
    # Class variable to hold the single instance of the webdriver_manager class
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Check if an instance of the class already exists
        if not cls._instance:
            # If not, create a new instance and assign it to the class variable
            cls._instance = super(WebdriverManager, cls).__new__(cls, *args, **kwargs)
        # Return the existing instance, ensuring only one instance of the class exists
        return cls._instance

    def __init__(self):
        # Check if the instance has already been initialized with the necessary attributes
        if not hasattr(self, 'open_drivers'):
            # Initialize an empty list to keep track of all open web drivers
            self.open_drivers = []
            # Set the URL for the Selenium server
            self.selenium_url = 'http://localhost:4444/wd/hub'
            # Initialize the options for the Firefox web driver
            self.options = webdriver.FirefoxOptions()
            # Initialize logger
            self.logger = logging.getLogger(__name__)

    def create_driver(self):
        # Create a new web driver instance
        driver = webdriver.Remote(
            command_executor=self.selenium_url,
            options=self.options)
        # Add the new driver to the list of open drivers
        self.open_drivers.append(driver)
        self.logger.info(f"Driver created: {driver}, Total open drivers: {len(self.open_drivers)}")
        # Return the newly created driver
        return driver

    def dispose_driver(self, driver):
        # Check if the driver is in the list of open drivers
        if driver in self.open_drivers:
            # Close the driver
            driver.quit()
            # Remove the driver from the list of open drivers
            self.open_drivers.remove(driver)
            self.logger.info(f"Closing driver: {driver}, Total open drivers: {len(self.open_drivers)}")
        else:
            # If the driver is not in the list, log an error
            self.logger.error(f"Attempted to close driver not in open drivers list: {driver}")