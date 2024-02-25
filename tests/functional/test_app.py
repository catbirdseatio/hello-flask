import pytest

from app import app


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to Website App" in response.data


def test_about_page(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert b"This is the about page of Website App" in response.data


def test_admin_is_error(client):
    response = client.get("/admin")
    assert response.status_code == 403


def test_error_404(client):
    response = client.get("/green")
    assert response.status_code == 404


def test_error_405(client):
    response = client.post("/")
    assert response.status_code == 405


def test_error_500(client):
    response = client.get("/error")
    assert response.status_code == 500


def test_get_write_message(client):
    response = client.get("/message/write")
    assert response.status_code == 200
    assert b"Add Message" in response.data
    assert b"<input" in response.data


def test_post_write_message(capsys, client):
    message = "Hello from Pytest!"
    response = client.post(
        "/message/write", data={"message": message}, follow_redirects=True
    )

    # test the print statement
    captured = capsys.readouterr()
    assert f"Message: {message}" in captured.out

    # test the response
    assert response.status_code == 200
    assert bytes(message, "utf-8") in response.data
    assert b"Welcome to Website App" in response.data
