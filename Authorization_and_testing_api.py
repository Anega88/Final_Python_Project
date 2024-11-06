from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import config
import requests


class Authorization_and_testing_api:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self._driver = None

def connect_to_api(self, endpoint, params=None):
        """Connects to the API using the provided API key and endpoint."""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raises an error for unsuccessful responses
        return response.json()