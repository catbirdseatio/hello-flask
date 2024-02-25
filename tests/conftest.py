import os
import pytest

from project import create_app, db
from project.models import Message


@pytest.fixture(scope='module')
def app():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    _app = create_app()

    with _app.app_context():
         db.create_all()
         yield _app
         db.drop_all()


@pytest.fixture(scope='module')
def client(app):
    with app.test_client() as test_client:
        yield test_client

@pytest.fixture(scope='module')
def message():
        return Message("Hello Python!")
