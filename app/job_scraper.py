import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from app.job_writer import JobWriter

class JobScraper:
    def __init__(self, driver_manager, target_job_titles):
        self.driver_manager = driver_manager
        self.target_job_titles = target_job_titles
        self.processed_ids = set()
        self.job_writer = JobWriter()

    def scrape_jobs(self, company_url):
        """Scrape jobs from a specific company URL."""
        jobs = []
        today = True
        start_time = time.time()  # Add start time
        
        self.driver_manager.driver.get(company_url)
        try:
            while today:
                # Add timeout check
                if time.time() - start_time > 20:
                    print(f"Timeout reached for {company_url}")
                    break
                    
                time.sleep(2)
                self.driver_manager.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//li[@class="css-1q2dra3"]')))
                
                job_elements = self.driver_manager.driver.find_elements(
                    By.XPATH, '//li[@class="css-1q2dra3"]')
                
                for job_element in job_elements:
                    job = self._process_job_element(job_element)
                    if job:
                        if job['posted_on'] == "Posted Today" or job['posted_on'] == "Posted Yesterday":
                            if job['id'] not in self.processed_ids:
                                self.job_writer.write_job(job['title'], job['id'], job['posted_on'], job['url'])
                                self.processed_ids.add(job['id'])
                        else:
                            today = False
                            break
                if not today:
                    break
        except Exception as e:
            print(f"An error occurred while processing {company_url}: {str(e)}")
        return jobs

    def _process_job_element(self, job_element):
        """Process individual job element and return job data if valid."""
        try:
            job_title_element = job_element.find_element(By.XPATH, './/h3/a')
            job_id_element = job_element.find_element(
                By.XPATH, './/ul[@data-automation-id="subtitle"]/li')
            posted_on_element = job_element.find_element(
                By.XPATH, 
                './/dd[@class="css-129m7dg"][preceding-sibling::dt[contains(text(),"posted on")]]')
            
            job_title = job_title_element.text
            job_href = job_title_element.get_attribute('href')  # Gets the href (URL) of the job
            # Filter jobs based on target job titles and exclude senior/staff positions
            if (not any(title.lower() in job_title.lower() for title in self.target_job_titles) or 
                any(excluded in job_title.lower() for excluded in ['senior', 'staff', 'principal', 'lead', 'sr', 'sr.', 'manager'])):
                return None
                
            return {
                'title': job_title,
                'id': job_id_element.text,
                'posted_on': posted_on_element.text,
                'url': job_href
            }
            
        except Exception as element_error:
            print(f"Failed to process job element: {str(element_error)}")
            return None