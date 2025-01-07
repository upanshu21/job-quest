import asyncio
from app.config.config_handler import ConfigHandler
from app.config.driver_manager import DriverManager
from app.job_scraper import JobScraper
from app.telegram.bot import NotificationTelegram


class JobScraperApp:
    def __init__(self):
        self.config = ConfigHandler()
        self.max_concurrent_tasks = 2
        self.notification = NotificationTelegram()

    async def scrape_company(self, company_url):
        """Asynchronously scrape jobs for a single company."""
        driver_manager = DriverManager()
        await driver_manager.initialize_driver_async()  
        job_scraper = JobScraper(driver_manager, self.config.target_job_titles)

        try:
            print(f"Scraping jobs from {company_url}...")
            await job_scraper.scrape_jobs(company_url) 
        except Exception as e:
            print(f"Error scraping {company_url}: {e}")
        finally:
            await driver_manager.close_driver_async() 

    async def run_scraper(self):
        """Run the scraper for all configured company URLs."""
        tasks = []
        semaphore = asyncio.Semaphore(self.max_concurrent_tasks)

        async def scrape_with_semaphore(company_url):
            async with semaphore:
                await self.scrape_company(company_url)

        for company_url in self.config.company_urls:
            tasks.append(scrape_with_semaphore(company_url))

        await asyncio.gather(*tasks)

    async def load_configuration(self):
        """Load configuration asynchronously."""
        print("Loading configuration...")
        await self.config.load_config() 

    async def run(self):
        """Main application loop."""
        try:
            await self.load_configuration() 
            while True:
                print("Starting job scraping...")
                await self.run_scraper()
                print("Waiting for the next run (30 minutes)...")
                self.notification.send_job_notification("Waiting for the next run (30 minutes)...")
                await asyncio.sleep(1800) 
        except Exception as e:
            print(f"Error occurred: {e}")


