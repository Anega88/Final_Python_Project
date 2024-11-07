import pytest
import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.ui
def test_search_movie_main_page(auth_ui):
    """Sample UI test."""
    driver = auth_ui._driver

    # Ищем фильм
    auth_ui.search_main_page(config.movie_to_search)

    try:
        # Проверяем, есть ли результаты поиска
        if driver.find_elements(By.CSS_SELECTOR, '.search_results'):
            # Если результаты поиска присутствуют, проверяем, что фильм отображается
            film_name_element = driver.find_element(By.CSS_SELECTOR, '.search_results .name a')
            # Приводим текст к нижнему регистру и убираем пробелы
            assert film_name_element.text.strip().lower() == config.movie_to_search.strip().lower(), "Film name is not as expected."
        elif driver.find_elements(By.CSS_SELECTOR, 'h2.textorangebig'):
            # Если сообщение о том, что ничего не найдено, присутствует
            no_results_message = driver.find_element(By.CSS_SELECTOR, 'h2.textorangebig').text
            assert no_results_message == "К сожалению, по вашему запросу ничего не найдено...", "Unexpected message when no results found."
        else:
            assert False, "No search results or error message found."

    except Exception as e:
        assert False, f"Search for '{config.movie_to_search}' resulted in an error: {e}"
    

@pytest.mark.ui
def test_search_actor_main_page(auth_ui):
    driver = auth_ui._driver
    auth_ui.search_main_page_actor(config.actor)
    
    try:
        # Ожидаем, пока появится страница с результатами поиска
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search_results')))
        
        # Проверяем наличие и количество результатов
        search_results_text = driver.find_element(By.CSS_SELECTOR, '.search_results_topText').text
        print(f"Results text: {search_results_text}")  # Отладочный вывод
        
        # Извлекаем количество результатов из текста с помощью регулярного выражения
        import re
        match = re.search(r'результаты: (\d+)', search_results_text)
        
        if match:
            results_count = int(match.group(1))
            assert results_count > 0, "No search results found for the actor."
            
            # Проверяем, что имя актера отображается на странице
            actor_name_element = driver.find_element(By.CSS_SELECTOR, '.search_results_topText b')
            
            # Сравниваем имя актера с ожидаемым
            assert actor_name_element.text.strip().lower() == config.actor.strip().lower(), "Actor name is not as expected."
        else:
            assert False, "Results count not found in the search results text."
        
    except Exception as e:
        assert False, f"Search for '{config.actor}' resulted in an error: {e}"

    
@pytest.mark.ui
def test_extended_search_movie(auth_ui):
    driver = auth_ui._driver
    expected_movie_text = f"{config.movie_to_search} ({config.movie_year})"
    
    # Выполнение расширенного поиска
    auth_ui.extended_search_movie(config.movie_to_search, config.movie_year, config.country, config.actor, config.genre)
    auth_ui.click_extended_search_button()  

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
    
    
@pytest.mark.ui
def test_open_reviews(auth_ui):
    driver = auth_ui._driver
    auth_ui.open_reviews(config.movie_name)
    all_reviews_label = driver.find_element(By.XPATH, '//span[text()="Все:"]')
    
    # Находим количество рецензий в следующем элементе <b>
    all_reviews_count = all_reviews_label.find_element(By.XPATH, 'following-sibling::b').text

    # Преобразуем строку в число
    number_of_reviews = int(all_reviews_count)

    # Assert для проверки, что количество рецензий больше 0
    assert number_of_reviews > 0, f"Expected at least one review, but found {number_of_reviews}."

   
@pytest.mark.ui
def test_open_filmography(auth_ui):
    auth_ui.open_filmography(config.actor)

    # Предположим, что на странице с фильмографией есть заголовок с именем актера
    wait = WebDriverWait(auth_ui._driver, 30)
    actor_header = wait.until(EC.presence_of_element_located((By.XPATH, f'//h1[contains(text(), "{config.actor}")]')))
    
    # Убедимся, что заголовок содержит имя актера
    assert actor_header.is_displayed(), f"Фильмография для актера '{config.actor}' не открылась."

    # Проверяем наличие элемента с количеством фильмов
    film_count_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.styles_subtitle__V93vt')))
    
    # Получаем текст и извлекаем количество фильмов
    film_count_text = film_count_element.text
    
    # Извлекаем только числовую часть из строки (например, "69 фильмов" станет "69")
    film_count = int(film_count_text.split()[0])  # или используйте регулярное выражение для более сложных случаев

    # Убедимся, что количество фильмов больше 0
    assert film_count > 0, f"Не найдено фильмов для актера '{config.actor}'. Количество фильмов: {film_count_text}."



