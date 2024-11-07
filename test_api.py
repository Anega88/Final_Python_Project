import pytest
from Authorization_and_testing_api import Authorization_and_testing_api
import config

@pytest.mark.api
@pytest.fixture(scope="function")
def auth():
    """Fixture to set up the Authorization API client."""
    return Authorization_and_testing_api(config.base_url_api, config.auth_token)

@pytest.mark.api
def test_search_id_movie(auth):
    """API test for retrieving movie details."""
    response = auth.search_movie_by_id(config.id_movie) 
    
    # Проверка, что ответ в формате JSON содержит ключ 'id'
    assert "id" in response.json(), "Response does not contain 'id' key"
    assert response.json()["id"] == config.id_movie, f"Expected movie ID to be {config.id_movie} but got {response.json()['id']}"
    assert "name" in response.json(), "Response does not contain 'name' key"
    movie_name = response.json()["name"]
    assert movie_name == config.movie_to_search, f"Expected movie name to be '{config.movie_to_search}' but got '{movie_name}'"

@pytest.mark.api
def test_movie_search(auth):
    """API test for searching a movie."""
    response = auth.search_movie()  # Вызов метода search_movie, который формирует запрос с параметрами
    
    data = response.json()
    
    # Проверка наличия данных в ответе
    assert "docs" in data, "Response does not contain 'docs' key"
    assert data["docs"], "Response 'docs' key contains an empty list"
    
    # Проверка данных первого найденного фильма
    first_movie = data["docs"][0]
    
    # Проверка названия
    assert "name" in first_movie, "First movie does not contain 'name' key"
    assert config.search_query.lower() in first_movie["name"].lower(), f"Expected query '{config.search_query}' in movie name but got {first_movie['name']}"
    
    # Проверка года выпуска
    assert "year" in first_movie, "First movie does not contain 'year' key"
    assert first_movie["year"] == config.movie_year_api, f"Year does not match {config.movie_year_api}"

    
    # Проверка жанров
    genres = [genre["name"] for genre in first_movie.get("genres", [])]
    assert config.genre_api_first in genres, f"Genre {config.genre_api_first} not found in movie genres"
    assert config.genre_api_second in genres, f"Genre {config.genre_api_second} not found in movie genres"
    
    # Проверка стран
    countries = [country["name"] for country in first_movie.get("countries", [])]
    assert config.country_api in countries, f"Country {config.country_api} not found in movie countries"
       
    # Проверка рейтингов
    assert "rating" in first_movie, "First movie does not contain 'rating' key"
    assert "kp" in first_movie["rating"], "No 'kp' rating found in movie ratings"
    min_rate, max_rate = map(float, config.rating.split("-"))
    movie_rating = first_movie['rating']["kp"]
    assert min_rate <= movie_rating<= max_rate, f"Movie rating {movie_rating} is not in the range {min_rate}-{max_rate}"

@pytest.mark.api
def test_actor_search(auth):
    """API test for searching a movie."""
    response = auth.search_actor()  # Вызов метода search_actor, который формирует запрос с параметрами
    
    data = response.json()
    
    # Проверка наличия данных в ответе
    assert "docs" in data, "Response does not contain 'docs' key"
    assert data["docs"], "Response 'docs' key contains an empty list"
    
    # Проверка данных первого найденного актера
    first_actor = data["docs"][0]
    
    # Проверка имени
    assert "name" in first_actor, "First movie does not contain 'name' key"
    assert config.actor_api.lower() in first_actor["name"].lower(), f"Expected query '{config.actor_api}' in movie name but got {first_actor['name']}"

@pytest.mark.api
def test_alternative_search(auth):
    """API test for searching"""
    response = auth.alternative_searching()

    if 'error' in response:
        pytest.fail(f"API returned an error: {response['error']}")

    data = response
    assert "docs" in data, "'docs' key not found in response"
    assert isinstance(data["docs"], list), "'docs' is not a list"

    # Проверяем, что хотя бы один фильм в списке содержит ожидаемые ключи
    if data["docs"]:
        movie = data["docs"][0]
        assert "id" in movie, "'id' key not found in movie"
        assert "name" in movie, "'name' key not found in movie"
        assert "rating" in movie, "'rating' key not found in movie"
        assert "kp" in movie["rating"], "'kp' rating not found in movie"
        assert "description" in movie, "'description' key not found in movie"
        assert "genres" in movie, "'genres' key not found in movie"
        assert isinstance(movie["genres"], list), "'genres' is not a list"

        # Проверяем, что количество элементов соответствует ожиданиям
        assert data["limit"] == 1, f"Expected limit of 1, but got {data['limit']}"
        assert data["page"] == 1, f"Expected page 1, but got {data['page']}"
     
        # Проверка периода, что год фильма в пределах указанного диапазона
        min_year, max_year = map(int, config.years.split("-"))
        movie_year = movie["year"]
        assert min_year <= movie_year <= max_year, f"Movie year {movie_year} is not in the range {min_year}-{max_year}"

        # Проверка рейтинга, что рейтинг фильма в пределах указанного
        min_rate, max_rate = map(int, config.rating.split("-"))
        movie_rating = movie['rating']["kp"]
        assert min_rate <= movie_rating<= max_rate, f"Movie rating {movie_rating} is not in the range {min_rate}-{max_rate}"

    else:
        print("No movies found in the response")

@pytest.mark.api
def test_genre_and_interval(auth):
    """API test for searching drama movies from 2000 to 2001."""
    # Выполняем запрос с параметрами
    response = auth.search_genre_and_interval()

    # Печать тела ответа для диагностики
    print(f"API response: {response}")

    # Проверка, что в ответе нет ошибки
    if 'error' in response:
        pytest.fail(f"API returned an error: {response['error']}")

    data = response  # Используем данные из ответа без дополнительного преобразования
    assert "docs" in data, "'docs' key not found in response"
    assert isinstance(data["docs"], list), "'docs' is not a list"
      
    # Проверяем, что хотя бы один фильм в списке содержит ожидаемые ключи
    if data["docs"]:
        movie = data["docs"][0]
        assert "id" in movie, "'id' key not found in movie"
        assert "name" in movie, "'name' key not found in movie"
        assert "rating" in movie, "'rating' key not found in movie"
        assert "kp" in movie["rating"], "'kp' rating not found in movie"
        assert "description" in movie, "'description' key not found in movie"
        assert "genres" in movie, "'genres' key not found in movie"
        assert isinstance(movie["genres"], list), "'genres' is not a list"
    
    # Проверка, что жанр, переданный в запросе, присутствует в жанрах фильма
        genres = [genre["name"] for genre in movie["genres"]]
        assert config.genre in genres, f"Genre '{config.genre}' not found in movie genres: {genres}"

        # Проверка периода, что год фильма в пределах указанного диапазона
        min_year, max_year = map(int, config.years.split("-"))  # Преобразуем строку "2000-2001" в два числа
        movie_year = movie["year"]
        assert min_year <= movie_year <= max_year, f"Movie year {movie_year} is not in the range {min_year}-{max_year}"

    else:
        print("No movies found in the response")


    


