import csv
import pickle
import time
import uuid
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

# Define company URLs to scrape
company_urls = [
    # 'https://mastercard.wd1.myworkdayjobs.com/en-US/CorporateCareers',
    # 'https://fifththird.wd5.myworkdayjobs.com/en-US/53careers',
    # 'https://walmart.wd5.myworkdayjobs.com/en-US/WalmartExternal?locationCountry=bc33aa3152ec42d4995f4791a106ed09',
    'https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite?locationHierarchy1=2fcb99c455831013ea52fb338f2932d8',
    # Add more URLs as needed
]

# Define target job titles to filter
target_job_titles = ["Software Engineer", "Engineer", "Developer"]

for company_url in company_urls:
    if company_url not in job_ids_dict:
        job_ids_dict[company_url] = []

def scrape_jobs(company_url):
    """Scrape jobs from a specific company URL."""
    jobs_to_send = []
    jobs = []

    driver.get(company_url)
    try:
        today = True
        while today:
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH, '//li[@class="css-1q2dra3"]')))
            
            job_elements = driver.find_elements(By.XPATH, '//li[@class="css-1q2dra3"]')
            for job_element in job_elements:
                try:
                    job_title_element = job_element.find_element(By.XPATH, './/h3/a')
                    job_id_element = job_element.find_element(By.XPATH, './/ul[@data-automation-id="subtitle"]/li')
                    posted_on_element = job_element.find_element(By.XPATH, './/dd[@class="css-129m7dg"][preceding-sibling::dt[contains(text(),"posted on")]]')
                    
                    job_id = job_id_element.text
                    posted_on = posted_on_element.text
                    job_title = job_title_element.text

                    # Filter jobs based on target job titles
                    # if not any(title.lower() in job_title.lower() for title in target_job_titles):
                    #     continue

                    print(job_title, job_id, posted_on)

                except Exception as element_error:
                    print(f"Failed to process job element: {str(element_error)}")
                    continue  # Skip this job and continue with the next one


            #This is only needed if you want to scrape all pages, as the aim of the application is to get all the jobs posted today
            # this snipped is not needed for the current application. 

            # next_button = driver.find_element(By.XPATH, '//button[@data-uxi-element-id="next"]')
            # if "disabled" in next_button.get_attribute("class"):
            #     break
            # next_button.click()

    except Exception as e:
        print(f"An error occurred while processing {company_url}: {str(e)}")
    
    return jobs


def main():
    """Main function to orchestrate job scraping."""
    while True:
        all_jobs = []
        for company_url in company_urls:
            print(f"Scraping jobs from {company_url}...")
            company_jobs = scrape_jobs(company_url)
            all_jobs.extend(company_jobs)

        print("Waiting for the next run...")
        time.sleep(3600) 

if __name__ == "__main__":
    main()
