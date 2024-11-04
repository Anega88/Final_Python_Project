import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
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
        "titanic": True,
        "2012": True,
        "": True
    }

    for movie in movies_to_search.keys():
        auth.search_main_page(movie)
        # Добавьте ваши ассерты здесь, чтобы проверить результаты поиска
        # Проверка, что поле поиска не пустое
        search_input = driver.find_element(By.CSS_SELECTOR, 'input[name="kp_query"]')
        assert search_input.get_attribute('value') == movie, f"Search input value should be '{movie}'"

        # Очищаем поле поиска для следующего ввода
        auth.clear_search_field()