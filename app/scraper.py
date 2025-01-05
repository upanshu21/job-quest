import time
from app.config.config_handler import ConfigHandler
from app.config.driver_manager import DriverManager
from app.job_scraper import JobScraper

class JobScraperApp:
    def __init__(self):
        self.config = ConfigHandler()
        self.driver_manager = DriverManager()
        self.job_scraper = None

    def initialize(self):
        """Initialize the application components."""
        self.driver_manager.initialize_driver()
        self.job_scraper = JobScraper(
            self.driver_manager,
            self.config.target_job_titles
        )

    def run(self):
        """Main application loop."""
        try:
            self.initialize()
            while True:
                for company_url in self.config.company_urls:
                    print(f"Scraping jobs from {company_url}...")
                    self.job_scraper.scrape_jobs(company_url)

                print("Waiting for the next run (30 minutes)...")
                time.sleep(1800)
        finally:
            self.driver_manager.close_driver()

