from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import asyncio

class DriverManager:
    def __init__(self, driver_path="/opt/homebrew/bin/chromedriver"):
        self.driver_path = driver_path
        self.driver = None
        self.wait = None

    async def initialize_driver_async(self):
        """Asynchronously initialize and configure the Selenium WebDriver."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(self.driver_path)
        
        await asyncio.sleep(0) 
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    async def close_driver_async(self):
        """Asynchronously close the WebDriver."""
        if self.driver:
            await asyncio.sleep(0)  
            self.driver.quit()
