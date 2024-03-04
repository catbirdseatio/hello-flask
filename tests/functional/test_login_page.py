
class TestLoginPage:
    route = "users/login"

    def test_get_login_page(self, client):
        response = client.get(self.route)
        assert response.status_code == 200
        assert b"Login" in response.data
        assert b"Email" in response.data
        assert b"Password" in response.data
        assert response.data.count(b'<input class="input"') == 2
        assert b"Forgot your password?" in response.data


    def test_valid_login_and_logout(self, client, db_test_user):
        response = client.post(
            self.route,
            data={"email": "roderick@email.com", "password": "testpass1234"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Thanks for logging in, roderick@email.com" in response.data

        response = client.get("/users/logout", follow_redirects=True)
        assert response.status_code == 200
        assert b"You have logged out" in response.data

    def test_invalid_login(self, client, db_test_user):
        response = client.post(
            self.route,
            data={"email": "roderick@email.com", "password": "FakePassWerd"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Incorrect Login Credentials." in response.data
        assert b"Thanks for logging in, roderick@email.com" not in response.data
        assert b"You are already logged in!" not in response.data
    
    def test_valid_login_when_logged_in_already(self, client, log_in_default_user):
        response = client.post(
            self.route,
            data={"email": "roderick@email.com", "password": "testpass1234"},
            follow_redirects=True,
        )
        assert b"You are already logged in!" in response.data
    
    def test_invalid_logout_not_logged_in(self, client, db_test_user):
        response = client.get("/users/logout", follow_redirects=True)
        assert response.status_code == 200
        assert b"You have logged out." not in response.data
        assert b"Login" in response.data

    def test_invalid_logout_using_post(self, client, log_in_default_user):
        response = client.post(
            "/users/logout",
            data={},
            follow_redirects=True,
        )
        response.status == 405
        assert b"Method Not Allowed (405)" in response.data
