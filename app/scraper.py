import csv
import pickle
import time
import uuid
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Initialize or load job_ids_dict from file
try:
    with open('job_ids_dict.pkl', 'rb') as f:
        job_ids_dict = pickle.load(f)
except FileNotFoundError:
    job_ids_dict = {}

# Configure Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service("/opt/homebrew/bin/chromedriver")  # Replace with the path to ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)

# Load configuration from config.json
try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        company_urls = config['company_urls']
        target_job_titles = config['target_job_titles']
except FileNotFoundError:
    print("Error: config.json file not found")
    exit(1)
except json.JSONDecodeError:
    print("Error: Invalid JSON format in config.json")
    exit(1)
except KeyError as e:
    print(f"Error: Missing required key in config.json: {e}")
    exit(1)

for company_url in company_urls:
    if company_url not in job_ids_dict:
        job_ids_dict[company_url] = []

def scrape_jobs(company_url, today):
    """Scrape jobs from a specific company URL."""
    jobs_to_send = []
    jobs = []

    driver.get(company_url)
    try:
        while today:
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH, '//li[@class="css-1q2dra3"]')))
            
            job_elements = driver.find_elements(By.XPATH, '//li[@class="css-1q2dra3"]')
            curr = ""
            for job_element in job_elements:
                try:
                    job_title_element = job_element.find_element(By.XPATH, './/h3/a')
                    job_id_element = job_element.find_element(By.XPATH, './/ul[@data-automation-id="subtitle"]/li')
                    posted_on_element = job_element.find_element(By.XPATH, './/dd[@class="css-129m7dg"][preceding-sibling::dt[contains(text(),"posted on")]]')
                    
                    job_id = job_id_element.text
                    posted_on = posted_on_element.text
                    job_title = job_title_element.text

                    # Filter jobs based on target job titles and exclude senior/staff positions
                    # last debug point, remove for testing
                    if (not any(title.lower() in job_title.lower() for title in target_job_titles) or 
                        any(excluded in job_title.lower() for excluded in ['senior', 'staff'])):
                        continue
                    
                    if posted_on == "Posted Today":
                        print(job_title, job_id, posted_on)
                    else:
                        today = False


                except Exception as element_error:
                    print(f"Failed to process job element: {str(element_error)}")
                    continue  # Skip this job and continue with the next one


            #This is only needed if you want to scrape all pages, as the aim of the application is to get all the jobs posted today
            # this snipped is not needed for the current application. 

            next_button = driver.find_element(By.XPATH, '//button[@data-uxi-element-id="next"]')
            if "disabled" in next_button.get_attribute("class"):
                break
            next_button.click()

    except Exception as e:
        print(f"An error occurred while processing {company_url}: {str(e)}")
    
    return jobs


def main():
    """Main function to orchestrate job scraping."""
    while True:
        all_jobs = []
        for company_url in company_urls:
            print(f"Scraping jobs from {company_url}...")
            company_jobs = scrape_jobs(company_url, True)
            all_jobs.extend(company_jobs)

        print("Waiting for the next run...")
        time.sleep(3600) 

if __name__ == "__main__":
    main()
