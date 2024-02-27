class TestRegistration:
    def test_get_registration_page(self, client):
        response = client.get("/users/register")
        assert response.status_code == 200
        assert response.data.count(b'<input class="input"') == 2

    def test_post_registration_page_success(self, client):
        response = client.post(
            "/users/register",
            data={"email": "rod@example.com", "password": "Testpass321"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Thanks for registering, rod@example.com" in response.data

    def test_post_registration_page_fail_no_password(self, client):
        response = client.post(
            "/users/register",
            data={"email": "rod@example.com", "password": None},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Thanks for registering, rod@example.com" not in response.data
        assert b"This field is required." in response.data

    def test_post_registration_page_fail_duplicate_user(self, client):
        client.post(
            "/users/register",
            data={"email": "rod@example.com", "password": None},
            follow_redirects=True,
        )
        response = client.post(
            "/users/register",
            data={"email": "rod@example.com", "password": None},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert "rod@example.com already exists."
