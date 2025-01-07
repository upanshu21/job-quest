import aiofiles
import os

class JobWriter:
    def __init__(self, filename='jobs.csv'):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'x', encoding='utf-8') as f:
                f.write("Title,ID,Posted,URL\n")

    async def write_job(self, title, job_id, posted_on, url):
        """Asynchronously write job details to a CSV file.
        
        Args:
            title (str): The job title
            job_id (str): The unique job identifier
            posted_on (str): When the job was posted
            url (str): The URL of the job posting
        """
        escaped_title = f'"{title}"' if ',' in title else title
        escaped_id = f'"{job_id}"' if ',' in job_id else job_id
        escaped_posted = f'"{posted_on}"' if ',' in posted_on else posted_on
        escaped_url = f'"{url}"' if ',' in url else url

        async with aiofiles.open(self.filename, 'a', encoding='utf-8') as f:
            await f.write(f"{escaped_title},{escaped_id},{escaped_posted},{escaped_url}\n")
