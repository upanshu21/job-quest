import json
import os

class ConfigHandler:
    def __init__(self, config_path=None):
        if config_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.config_path = os.path.join(current_dir, 'config.json')
        else:
            self.config_path = config_path
        self.company_urls = []
        self.target_job_titles = []
        self.load_config()

    def load_config(self):
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as config_file:
                config = json.load(config_file)
                self.company_urls = config['company_urls']
                self.target_job_titles = config['target_job_titles']
        except FileNotFoundError:
            raise Exception("Error: config.json file not found")
        except json.JSONDecodeError:
            raise Exception("Error: Invalid JSON format in config.json")
        except KeyError as e:
            raise Exception(f"Error: Missing required key in config.json: {e}")