import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Authorization_and_testing import Authorization_and_testing
import config


@pytest.mark.api
@pytest.fixture(scope="module")
def auth():
    """Fixture to set up Authorization for API tests."""
    return Authorization_and_testing(config.base_url, config.auth_token)

def test_api_requests(auth):
    """Sample API test."""
    response = auth.connect_to_api("/movies", params={"title": "Inception"})
    assert response["status"] == "success"