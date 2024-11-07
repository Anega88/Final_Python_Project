import pytest
from Authorization_and_testing_api import Authorization_and_testing_api
from Authorization_and_testing_ui import Authorization_and_testing_ui
import config

@pytest.fixture(scope="function")
def auth_ui():
    """Fixture to set up and tear down the WebDriver."""
    auth = Authorization_and_testing_ui(config.base_url)
    driver = auth.setup_webdriver()
    yield auth
    auth.close_webdriver()

@pytest.fixture(scope="function")
def auth_api():
    """Fixture to set up the Authorization API client."""
    return Authorization_and_testing_api(config.base_url_api, config.auth_token)
