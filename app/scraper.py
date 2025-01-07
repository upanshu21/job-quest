import time
import concurrent.futures
from app.config.config_handler import ConfigHandler
from app.config.driver_manager import DriverManager
from app.job_scraper import JobScraper

class JobScraperApp:
    def __init__(self):
        self.config = ConfigHandler()
        self.driver_manager = DriverManager()
        self.job_scraper = None
        self.max_workers = 1  # Adjust based on your system's capabilities

    def scrape_company(self, company_url):
        """Scrape jobs for a single company."""
        try:
            # Each thread needs its own driver instance
            driver_manager = DriverManager()
            driver_manager.initialize_driver()
            job_scraper = JobScraper(driver_manager, self.config.target_job_titles)
            
            print(f"Scraping jobs from {company_url}...")
            job_scraper.scrape_jobs(company_url)
        finally:
            driver_manager.close_driver()

    def run(self):
        """Main application loop."""
        try:
            while True:
                # Create a thread pool and submit scraping tasks
                with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    executor.map(self.scrape_company, self.config.company_urls)

                print("Waiting for the next run (30 minutes)...")
                time.sleep(1800)
        except Exception as e:
            print(f"Error occurred: {e}")

