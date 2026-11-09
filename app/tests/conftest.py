import os
import pytest

# Variables configurables por entorno
URL_API = os.environ.get("URL_API", "http://localhost:8000")
URL_WEB = os.environ.get("URL_WEB", "http://localhost:8080")


@pytest.fixture
def url_api():
    return URL_API


@pytest.fixture
def url_web():
    return URL_WEB
