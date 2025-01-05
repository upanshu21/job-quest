class JobWriter:
    def __init__(self, filename='jobs.csv'):
        self.filename = filename
        # Create file with headers if it doesn't exist
        try:
            with open(self.filename, 'x', encoding='utf-8') as f:
                f.write("Title,ID,Posted,URL\n")
        except FileExistsError:
            pass

    def write_job(self, title, job_id, posted_on, url):
        """Write job details to a CSV file.
        
        Args:
            title (str): The job title
            job_id (str): The unique job identifier
            posted_on (str): When the job was posted
            url (str): The URL of the job posting
        """
        with open(self.filename, 'a', encoding='utf-8') as f:
            # Escape any commas in the fields
            escaped_title = f'"{title}"' if ',' in title else title
            escaped_id = f'"{job_id}"' if ',' in job_id else job_id
            escaped_posted = f'"{posted_on}"' if ',' in posted_on else posted_on
            escaped_url = f'"{url}"' if ',' in url else url
            
            f.write(f"{escaped_title},{escaped_id},{escaped_posted},{escaped_url}\n")