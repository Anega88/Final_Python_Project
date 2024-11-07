import requests
import config

class Authorization_and_testing_api:
    def __init__(self, base_url_api, api_key=None):
        self.base_url = base_url_api
        self.api_key = api_key

    def connect_to_api_with_params(self, params=None):
        """Запрос без обязательного эндпоинта, только параметры"""
        url = self.base_url  # Просто base_url, без добавления endpoint
        headers = {
            'X-API-KEY': config.auth_token,
            'accept': 'application/json'
            }

        response = requests.get(url, headers=headers, params=params)
        
        return response
    
    def connect_to_api_with_endpoint(self, endpoint, params=None):
        """Запрос с обязательным эндпоинтом и параметрами"""
        url = self.base_url + endpoint  # Добавляем endpoint к base_url
        headers = {
            'X-API-KEY': config.auth_token,
            'accept': 'application/json'
        }

        response = requests.get(url, headers=headers, params=params)
        
        return response
    
    def search_movie_by_id(self, movie_id):
        """Запрос для получения деталей фильма по ID"""
        endpoint = f"/{movie_id}"  # Эндпоинт в формате /movie/{id}
        params = {}  # Здесь параметры могут быть пустыми или дополнены
        return self.connect_to_api_with_endpoint(endpoint, params)

    def search_movie(self):
        """Performs a search query on the API."""
        endpoint = "/search"  # Здесь указано, что мы будем делать запрос к эндпоинту "search"
        params = {
            "page": config.page,
            "limit": config.limit,
            "query": config.search_query  # Параметры для поиска, включая поисковый запрос
            }
        return self.connect_to_api_with_endpoint(endpoint, params=params)

    def alternative_searching(self):
        params = {
            "page": config.page,
            "limit": config.limit,
            "releaseYears.start": config.years,
            "rating.kp": config.rating
            }

        # Логируем параметры запроса
        print(f"Request parameters: {params}")

        response = self.connect_to_api_with_params(params=params)

        # Логируем ответ для диагностики
        print(f"API response: {response.text}")

        return response.json()  # Попробуем преобразовать в JSON
    
    def search__and_interval(self):
            """Запрос для получения списка драм за указанный период."""
            params = {
                "page": config.page,
                "limit": config.limit,
                "year": config.years,
                "genres.name": config.genre
                }
            # Логируем параметры запроса
            print(f"Request parameters: {params}")

            response = self.connect_to_api_with_params(params=params)

            # Логируем ответ для диагностики
            print(f"API response: {response.text}")

            return response.json()  # Попробуем преобразовать в JSON
    
    def search_genre_and_interval(self):
            """Запрос для получения списка драм за указанный период."""
            params = {
                "page": config.page,
                "limit": config.limit,
                "year": config.years,
                "genres.name": config.genre
                }
            # Логируем параметры запроса
            print(f"Request parameters: {params}")

            response = self.connect_to_api_with_params(params=params)

            # Логируем ответ для диагностики
            print(f"API response: {response.text}")

            return response.json()  # Попробуем преобразовать в JSON

    def search_actor(self):
            """Performs a search query on the API."""
            endpoint = "/search"
            params = {
                "page": config.page,
                "limit": config.limit,
                "query": config.actor_api
                }
            return self.connect_to_api_with_endpoint(endpoint, params=params)

