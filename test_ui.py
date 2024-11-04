import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Authorization_and_testing import Authorization_and_testing

base_url = "https://www.kinopoisk.ru/"


@pytest.mark.ui
@pytest.fixture(scope="module")
def auth():
    """Fixture to set up and tear down the WebDriver."""
    auth = Authorization_and_testing(base_url)
    driver = auth.setup_webdriver()
    yield auth
    auth.close_webdriver()

def test_functional_ui(auth):
    """Sample UI test."""
    driver = auth._driver
    
    movies_to_search = {
        "титаник": True,
        "ТИТАНИК": True,
        "titanic": True,
        "TITANIC": True,
        "2012": True,
        "24 часа": True,
        "а": True,
        "": True,
        "11.09.2001": True,
        "11-11-11": True,
        "стражи галактики": True,
        "стажи гааактики": True,
        "strazhi": True,
        "стр": True,
    }

    for movie in movies_to_search.keys():
        auth.search_main_page(movie)