import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import json
from datetime import datetime

# Load environment variables
load_dotenv()

class ConfigNocoDB:
    def __init__(self):
        self.BASE_URL = os.getenv('NOCO_URL')
        self.headers = {
            'xc-token': os.getenv('API_TOKEN'),
            'Content-Type': 'application/json',
            'Accept': 'application/json' 
        }

    def get_data(self):
        response = requests.get(self.BASE_URL, headers=self.headers, params={"offset": 0, "limit": 25})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error Fetching Data: {response.status_code} - {response.text}")
            return None
    

    def extract_company_name(self, url):
        parsed_url = urlparse(url)
        domain_parts = parsed_url.netloc.split(".")
        return domain_parts[0] 


    def post_data(self, job_data):
        company_name = self.extract_company_name(job_data["url"])
        today_date = datetime.today().strftime('%Y-%m-%d') 
        payload = {
            "Company name": company_name, 
            "Position": job_data["title"], 
            "Data Posted": today_date, 
            "Apply": job_data["url"],
            "role_id": job_data["id"]
        }
        response = requests.post(self.BASE_URL, headers=self.headers, json=payload)
        if response.status_code in [200, 201]: 
            return "Record with ID: {} created successfully".format(response.json().get("id"))
        else:
            return "Error creating record: {} - {}".format(response.status_code, response.text)


    def check_if_job_exists(self, job_id) -> bool:
        response = requests.get(
            self.BASE_URL, 
            headers=self.headers, 
            params={"limit": 30, "offset": 0}  
        )
        if response.status_code == 200:
            records = response.json().get("list", [])
            for record in records:
                if record.get("role_id") == job_id:
                    return True
        return False 

