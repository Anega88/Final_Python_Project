from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests

class Authorization_and_testing:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self._driver = None

    def setup_webdriver(self):
        """Initializes the WebDriver for Selenium tests and opens the specified URL."""
        self._driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self._driver.get(self.base_url)
        self._driver.implicitly_wait(4)
        self._driver.maximize_window()
        self.click_captcha_checkbox()  # Нажимаем на чекбокс сразу после загрузки страницы
        return self._driver

    def click_captcha_checkbox(self):
        """Clicks the CAPTCHA checkbox."""
        try:
            captcha_checkbox = WebDriverWait(self._driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#js-button'))
                 )
            captcha_checkbox.click()
        except Exception as e:
            print(f"Failed to click CAPTCHA checkbox: {e}")


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
    
    def search_main_page(self, movie_name):
        self.movie_name = movie_name
        search_input = self._driver.find_element(By.CSS_SELECTOR, 'input[name="kp_query"]')
        search_input.clear()  # Очищаем поле поиска перед вводом
        search_input.send_keys(movie_name)
        self.click_search_button()

    def click_search_button(self):
        """Clicks the search button."""
        try:
            # Пробуем найти первую кнопку (по значку поиска)
            search_button_svg = self._driver.find_element(By.CSS_SELECTOR, 'svg.styles_iconActive__dJx1_')
            search_button_svg.click()  # Нажимаем на первую кнопку поиска
        except Exception as e:
            print(f"Error clicking SVG search button: {e}")
            try:
                # Если первая кнопка не найдена, пробуем нажать на альтернативную кнопку
                search_button_alt = self._driver.find_element(By.CSS_SELECTOR, 'input.el_18.submit.nice_button')
                search_button_alt.click()
            except Exception as e_alt:
                print(f"Error clicking alternative search button: {e_alt}")


    def clear_search_field(self):
        """Clears the search input field."""
        search_input = self._driver.find_element(By.CSS_SELECTOR, 'input[name="kp_query"]')
        search_input.clear()  # Очищает поле поиска


    def extended_search_movie(self, movie_name, year, country, actor, genre):
        self.movie_name = movie_name
        self.year = year
        self.country = country
        self.actor = actor
        self.genre = genre

        wait = WebDriverWait(self._driver, 15)

        try:
            input_extended_search = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[aria-label="Расширенный поиск"]'))).click()
            
            input_movie_name = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#find_film')))
            input_movie_name.send_keys(movie_name)

            input_year = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#year')))
            input_year.send_keys(year)

            input_country = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#country')))
            input_country.send_keys(country)

            input_actor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="m_act[actor]"]')))
            input_actor.send_keys(actor)

            genre_dropdown = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#m_act\\[genre\\]')))
            genre_option = genre_dropdown.find_element(By.XPATH, f'//option[text()="{genre}"]')
            genre_option.click()

            search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.el_18.submit.nice_button')))
            search_button.click()
        
        except Exception as e:
            print(f"Ошибка при выполнении расширенного поиска: {e}")


    def open_reviews(self, movie_name):
        driver = self._driver
        wait = WebDriverWait(driver, 30)

        # Поиск фильма на главной странице
        self.search_main_page(movie_name)
        self.click_search_button()

        # Ожидание появления фильма в результатах поиска и клик по нему
        movie_link = wait.until(EC.element_to_be_clickable((By.XPATH, f'//a[text()="{movie_name}"]')))
        movie_link.click()

        # Ожидание появления ссылки на "Рецензии зрителей"
        reviews = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.styles_reviewCountLight__XNZ9P.styles_reviewCount__w_RrM'))).click()
        reviews_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Рецензии зрителей")))


        # Клик по ссылке "Рецензии зрителей"
        reviews_link.click()

   

    def close_webdriver(self):
        """Closes the WebDriver."""
        if self._driver:
            self._driver.quit()
