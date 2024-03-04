from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from project import mail

class TestPasswordReset:
    route = "/users/password_reset"
    def test_get_password_reset(self, client):
        response = client.get(self.route)
        assert b"Password Reset"
        assert response.data.count(b'<input class="input"') == 1
        assert b"Submit" in response.data
    
    def test_post_password_reset_via_email_page_valid(self, client, confirmed_db_test_user):
        with mail.record_messages() as outbox:
            response = client.post(self.route,
                                   data={"email": "roderick@email.com"}, follow_redirects=True)
            assert response.status_code == 200
            assert b"Please check your email for a password reset link" in response.data
            assert len(outbox) == 1
            assert outbox[0].subject == "Flask App - Password Reset Requested"
            assert outbox[0].sender == "leighmforrest@gmail.com"
            assert outbox[0].recipients[0] == "roderick@email.com"
            assert "http://localhost/users/process_password_reset" in outbox[0].html
    
    def test_post_password_reset_via_email_page_invalid(self, client):
        with mail.record_messages() as outbox:
            response = client.post(self.route,
                                   data={"email": "roderick@example.com"}, follow_redirects=True)
            assert response.status_code == 200
            assert len(outbox) == 0
            assert b"Invalid user address." in response.data
    
    def test_post_password_reset_via_email_page_not_confirmed(self, client, db_test_user):
        with mail.record_messages() as outbox:
            response = client.post(self.route,
                                   data={"email": "roderick@email.com"}, follow_redirects=True)
            assert response.status_code == 200
            assert len(outbox) == 0
            assert b"Your email must be confirmed before attempting a password reset." in response.data
    
    def test_get_password_reset_valid_token(self, client):
        password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = password_reset_serializer.dumps('roderick@email.com', 'password-reset-salt')

        response = client.get(f"/users/process_password_reset/{token}", follow_redirects=True)
        assert response.status_code == 200
        assert b"Password Reset" in response.data
        assert b"New Password" in response.data
        assert b"Submit" in response.data
    
    def test_get_password_reset_valid_token(self, client):
        token = "ReallyBadToken"

        response = client.get(f"/users/process_password_reset/{token}", follow_redirects=True)
        assert response.status_code == 200
        assert b"Password Reset" not in response.data
        assert b"The password reset link is invalid or has expired." in response.data
    
    def test_post_password_reset_valid_token(self, client, reset_db_test_user_password):
        password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = password_reset_serializer.dumps('roderick@email.com', 'password-reset-salt')

        response = client.post(f"/users/process_password_reset/{token}",
                               data={'password': 'FlaskIsTheBestFramework'}, follow_redirects=True)
        assert response.status_code == 200
        print(response.data)
        assert b"Your password has been updated." in response.data
    
    def test_post_password_reset_invalid_token(self, client, db_test_user):
        # Note: db_test_user fixture needed for app context
        token = "ReallyBadToken"

        response = client.post(f"/users/process_password_reset/{token}",
                               data={'password': 'FlaskIsTheBestFramework'}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Your password has been updated." not in response.data
        assert b"The password reset link is invalid or has expired."
