import os
import pytest

from project import create_app, db
from project.models import Message, User


@pytest.fixture(scope="module")
def app():
    _app = create_app()
    os.environ["CONFIG_TYPE"] = "config.TestingConfig"
    _app.extensions['mail'].suppress = True

    with _app.app_context():
        db.create_all()
        yield _app
        db.drop_all()


@pytest.fixture(scope="module")
def client(app):
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture(scope="module")
def message():
    return Message("Hello Python!")


@pytest.fixture(scope="module")
def new_user():
    user = User("roderick@email.com", "testpass1234")
    return user


@pytest.fixture(scope="module")
def db_test_user(new_user):
    db.session.add(new_user)
    db.session.commit()

    yield new_user

    db.session.delete(new_user)
    db.session.commit()


@pytest.fixture(scope="function")
def log_in_default_user(client, db_test_user):
    client.post(
        "/users/login",
        data={"email": "roderick@email.com", "password": "testpass1234"},
        follow_redirects=True,
    )
    yield
    client.get("/users/logout", follow_redirects=True)
