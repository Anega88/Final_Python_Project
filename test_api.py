import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Authorization_and_testing_api import Authorization_and_testing_api
import config


@pytest.mark.api
@pytest.fixture(scope="function")
def auth():
    """Fixture to set up and tear down the WebDriver."""
    auth = Authorization_and_testing_api(config.base_url, config.auth_token)

@pytest.mark.api
def test_api_requests(auth):
    """Sample API test."""
    response = auth.connect_to_api("/movies", params={"title": "Inception"})
    assert response["status"] == "success"