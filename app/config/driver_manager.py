from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

class DriverManager:
    def __init__(self, driver_path="/opt/homebrew/bin/chromedriver"):
        self.driver_path = driver_path
        self.driver = None
        self.wait = None
        
    def initialize_driver(self):
        """Initialize and configure the Selenium WebDriver."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
    def close_driver(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()