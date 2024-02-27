class TestPages:
    def test_index_page(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert b"Welcome to Website App" in response.data

    def test_about_page(self, client):
        response = client.get("/about")
        assert response.status_code == 200
        assert b"This is the about page of Website App" in response.data

    def test_get_write_message(self, client):
        response = client.get("/message/write")
        assert response.status_code == 200
        assert b"Add Message" in response.data
        assert b"<input" in response.data

    def test_post_write_message(self, client):
        message = "Hello from Pytest!"
        response = client.post(
            "/message/write", data={"message": message}, follow_redirects=True
        )

        # test the response
        assert response.status_code == 200
        assert bytes(message, "utf-8") in response.data
        assert b"Welcome to Website App" in response.data

    def test_post_write_message_print_statement(self, capsys, client):
        message = "Hello from Pytest!"
        response = client.post(
            "/message/write", data={"message": message}, follow_redirects=True
        )

        # test the print statement
        captured = capsys.readouterr()
        assert f"Message: {message}" in captured.out