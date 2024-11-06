from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import config


class Authorization_and_testing_ui:
    def __init__(self, base_url):
        self.base_url = base_url
        self._driver = None

    def setup_webdriver(self):
        """Initializes the WebDriver for Selenium tests and opens the specified URL."""
        self._driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self._driver.get(self.base_url)
        self._driver.implicitly_wait(4)
        self._driver.maximize_window()
        self.add_auth_token_to_cookies(config.auth_token)
        self.click_captcha_checkbox()
        return self._driver
    
    def add_auth_token_to_cookies(self, token):
        """Adds the authorization token to browser cookies."""
        self._driver.add_cookie({
            "name": "auth_token",  # Имя куки для токена авторизации
            "value": token,
            "path": "/",
            "domain": "www.kinopoisk.ru"  # Убедитесь, что домен совпадает с вашим сайтом
        })
        self._driver.refresh() 

    def click_captcha_checkbox(self):
        """Clicks the CAPTCHA checkbox."""
        try:
            captcha_checkbox = WebDriverWait(self._driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#js-button'))
                 )
            captcha_checkbox.click()
        except Exception as e:
            print(f"Failed to click CAPTCHA checkbox: {e}")

    
    def search_main_page(self, movie_name):
        self.movie_name = movie_name
        search_input = self._driver.find_element(By.CSS_SELECTOR, 'input[name="kp_query"]')
        search_input.clear()  # Очищаем поле поиска перед вводом
        search_input.send_keys(movie_name)
        self.click_main_search_button()

    def search_main_page_actor(self, actor):
        self.actor = actor
        search_input = self._driver.find_element(By.CSS_SELECTOR, 'input[name="kp_query"]')
        search_input.send_keys(actor)
        self.click_main_search_button()


    def click_main_search_button(self):
        """Clicks the main SVG search button."""
        try:
            search_button_svg = WebDriverWait(self._driver, 10).until(
                 EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "styles_submit__2AIpj") and @aria-label="Найти"]'))
                )
            search_button_svg.click()
        except Exception as e:
            print(f"Error clicking main SVG search button: {e}")

    def click_extended_search_button(self):
        search_button_alt = self._driver.find_element(By.CSS_SELECTOR, 'input[class="el_18 submit nice_button"]')
        search_button_alt.click()
            

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

            genre_dropdown = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'id="m_act[genre]"')))
            genre_option = genre_dropdown.find_element(By.XPATH, f'//option[@value="{genre}"]')
            genre_option.click()
        
        except Exception as e:
            print(f"Ошибка при выполнении расширенного поиска: {e}")


    def open_reviews(self, movie_name):
        driver = self._driver
        wait = WebDriverWait(driver, 30)

        # Поиск фильма на главной странице
        self.search_main_page(movie_name)
        self.click_main_search_button()

        # Ожидание появления фильма в результатах поиска и клик по нему
        movie_link = wait.until(EC.element_to_be_clickable((By.XPATH, f'//a[text()="{movie_name}"]')))
        movie_link.click()

        # Ожидание появления ссылки на "Рецензии зрителей"
        reviews = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.styles_reviewCountLight__XNZ9P.styles_reviewCount__w_RrM'))).click()
        reviews_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Рецензии зрителей")))

        # Клик по ссылке "Рецензии зрителей"
        reviews_link.click()


    def open_filmography(self, actor):
        driver = self._driver
        wait = WebDriverWait(driver, 30)

        self.search_main_page_actor(actor)
        self.click_main_search_button()

        # Ожидание появления фильма в результатах поиска и клик по нему
        actor_link = wait.until(EC.element_to_be_clickable((By.XPATH, f'//a[text()="{actor}"]')))
        actor_link.click()

        driver.execute_script("window.scrollBy(0, 2800)")
    
        # Прокрутка до кнопки "Фильмография" с использованием ActionChains
        filmography_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-tid="9fd92bab"] .styles_title__skJ4z')))
        ActionChains(driver).scroll_to_element(filmography_button).perform()

        # Клик по кнопке "Фильмография"
        filmography_button.click()
    
        # Возвращаемся к основному контенту, если необходимо выполнять другие действия на странице
        driver.switch_to.default_content()
   

    def close_webdriver(self):
        """Closes the WebDriver."""
        if self._driver:
            self._driver.quit()
