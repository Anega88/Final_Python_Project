import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Authorization_and_testing import Authorization_and_testing
from time import sleep

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

    movie_to_search = "титаник"

    # Ищем фильм
    auth.search_main_page(movie_to_search)

    # Нажимаем кнопку поиска
    auth.click_search_button()

    try:
        # Проверяем, есть ли результаты поиска
        if driver.find_elements(By.CSS_SELECTOR, '.search_results'):
            # Если результаты поиска присутствуют, проверяем, что фильм отображается
            film_name_element = driver.find_element(By.CSS_SELECTOR, '.search_results .name a')
            assert film_name_element.text.lower() == movie_to_search, "Film name is not as expected."
        elif driver.find_elements(By.CSS_SELECTOR, 'h2.textorangebig'):
            # Если сообщение о том, что ничего не найдено, присутствует
            no_results_message = driver.find_element(By.CSS_SELECTOR, 'h2.textorangebig').text
            assert no_results_message == "К сожалению, по вашему запросу ничего не найдено...", "Unexpected message when no results found."
        else:
            assert False, "No search results or error message found."

    except Exception as e:
        assert False, f"Search for '{movie_to_search}' resulted in an error: {e}"

def test_extended_search_movie(auth):
    driver = auth._driver
    movie_name = "Титаник"
    movie_year = "1997"
    expected_movie_text = f"{movie_name} ({movie_year})"
    
    # Выполнение расширенного поиска
    auth.extended_search_movie(movie_name, movie_year, "США", "Леонардо ДиКаприо", "Комедия")
    auth.click_search_button()
    
    # Ожидание появления заголовка с фильмом
    try:
        h1_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1[data-tid="f22e0093"]'))
        )
        # Находим вложенный элемент <span> с названием фильма
        movie_element = h1_element.find_element(By.CSS_SELECTOR, 'span[data-tid="75209b22"]')
        assert movie_element.text == expected_movie_text, f"Expected '{expected_movie_text}', but got '{movie_element.text}'"
    except Exception as e:
        assert False, f"Movie '{expected_movie_text}' was not found in search results: {e}"

def test_open_reviews(auth):
    driver = auth._driver
    auth.open_reviews("Терминатор")
    all_reviews_label = driver.find_element(By.XPATH, '//span[text()="Все:"]')
    
    # Находим количество рецензий в следующем элементе <b>
    all_reviews_count = all_reviews_label.find_element(By.XPATH, 'following-sibling::b').text

    # Преобразуем строку в число
    number_of_reviews = int(all_reviews_count)

    # Assert для проверки, что количество рецензий больше 0
    assert number_of_reviews > 0, f"Expected at least one review, but found {number_of_reviews}."