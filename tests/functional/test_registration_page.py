from project import mail


class TestRegistration:
    def test_get_registration_page(self, client):
        response = client.get("/users/register")
        assert response.status_code == 200
        assert response.data.count(b'<input class="input"') == 2

    def test_post_registration_page_success(self, client):
        with mail.record_messages() as outbox:
            response = client.post(
                "/users/register",
                data={"email": "rod@example.com", "password": "Testpass321"},
                follow_redirects=True,
            )
            assert response.status_code == 200
            assert b"Thanks for registering, rod@example.com" in response.data

            assert len(outbox) == 1
            assert outbox[0].subject == 'Registration - Flask App'
            assert outbox[0].sender == 'leighmforrest@gmail.com'
            assert outbox[0].recipients[0] == 'rod@example.com'

    def test_post_registration_page_fail_no_password(self, client):
        response = client.post(
            "/users/register",
            data={"email": "rod@example.com", "password": None},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Thanks for registering, rod@example.com" not in response.data
        assert b"This field is required." in response.data

    def test_post_registration_page_fail_duplicate_user(self, client, db_test_user):
        response = client.post(
            "/users/register",
            data={"email": "roderick@email.com", "password": "testpass1234"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"roderick@email.com already exists." in response.data
