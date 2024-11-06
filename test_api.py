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

@pytest.mark.api
def test_movie_search(auth):
    """API test for searching a movie."""
    response = auth.search_movie()  # Вызов метода search_movie, который формирует запрос с параметрами
    
    # Преобразование ответа в JSON (Python словарь)
    data = response.json()
    
    # Печать ответа для диагностики
    print(data)
    
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
    assert first_movie["year"] == 1984, "Year does not match 1984"
    
    # Проверка жанров
    genres = [genre["name"] for genre in first_movie.get("genres", [])]
    assert "фантастика" in genres, "Genre 'фантастика' not found in movie genres"
    assert "боевик" in genres, "Genre 'боевик' not found in movie genres"
    
    # Проверка стран
    countries = [country["name"] for country in first_movie.get("countries", [])]
    assert "США" in countries, "Country 'США' not found in movie countries"
       
    # Проверка рейтингов
    assert "rating" in first_movie, "First movie does not contain 'rating' key"
    assert "kp" in first_movie["rating"], "No 'kp' rating found in movie ratings"
    assert first_movie["rating"]["kp"] >= 7, "Expected 'kp' rating to be 7 or higher"

@pytest.mark.api
def test_alternative_search(auth):
    """API test for searching"""
    response = auth.alternative_searching()

    # Проверяем, что в ответе нет ошибки
    if 'error' in response:
        pytest.fail(f"API returned an error: {response['error']}")

    data = response  # Это уже будет словарь с данными
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
    assert data["total"] == 25, f"Expected 25 total movies, but got {data['total']}"
    assert data["limit"] == 1, f"Expected limit of 1, but got {data['limit']}"
    assert data["page"] == 1, f"Expected page 1, but got {data['page']}"
    assert data["pages"] == 25, f"Expected 25 pages, but got {data['pages']}"



