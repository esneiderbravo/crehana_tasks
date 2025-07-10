import pytest
from unittest.mock import patch


@pytest.fixture(scope="session", autouse=True)
def disable_authentication():
    """
    Fixture to disable authentication for all tests.
    """
    patcher = patch("src.application.auth.require_authentication", lambda x: x)
    patcher.start()
    yield
    patcher.stop()


@pytest.fixture
def test_app():
    from src.main import app

    return app
