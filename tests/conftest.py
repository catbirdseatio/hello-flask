import os
import pytest
from project import create_app


@pytest.fixture(scope='module')
def app():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    yield create_app()


@pytest.fixture(scope='module')
def client(app):
    with app.test_client() as test_client:
        yield test_client