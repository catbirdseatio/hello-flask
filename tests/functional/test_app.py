from app import app


def test_index_page():
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert b"Welcome to Website App" in response.data


def test_about_page():
    with app.test_client() as client:
        response = client.get("/about")
        assert response.status_code == 200
        assert b"This is the about page of Website App" in response.data


def test_get_write_message():
    with app.test_client() as client:
        response = client.get("/message/write")
        assert response.status_code == 200
        assert b"Add Message" in response.data
        assert b'<input type="text" name="message">' in response.data


def test_post_write_message(capsys):
    message = "Hello from Pytest!"
    with app.test_client() as client:
        response = client.post(
            "/message/write", data={"message": message}, follow_redirects=True
        )

        # test the print statement
        captured = capsys.readouterr()
        assert f"message: {message}" in captured.out

        # test the response
        assert response.status_code == 200
        assert bytes(message, "utf-8") in response.data
        assert b"<h1>Welcome to Website App</h1>" in response.data
