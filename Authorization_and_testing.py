from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests


class Authorization_and_testing:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self._driver = None

    def setup_webdriver(self):
        """Initializes the WebDriver for Selenium tests and opens the specified URL."""
        self._driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self._driver.get(self.base_url)
        self._driver.implicitly_wait(4)
        self._driver.maximize_window()
        return self._driver

    def connect_to_api(self, endpoint, params=None):
        """
        Connects to the API using the provided API key and endpoint.
        Returns the API response.
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raises an error for unsuccessful responses
        return response.json()
    
    def search_main_page(self, movie_name):
        """Searches for a movie on the main page and clears the search field after each entry."""
        self.movie_name = movie_name
        search_input = self._driver.find_element(By.CSS_SELECTOR, 'input[name="kp_query"]')
        search_input.send_keys(movie_name)
        self.clear_search_field()

    def clear_search_field(self):
        """Clears the search input field."""
        search_input = self._driver.find_element(By.CSS_SELECTOR, 'input[name="kp_query"]')
        search_input.clear()  # Очищает поле поиска

    def close_webdriver(self):
        """Closes the WebDriver."""
        if self._driver:
            self._driver.quit()

    

