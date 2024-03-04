from itsdangerous import URLSafeTimedSerializer
from flask import current_app

from project import mail, db
from project.models import User


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
            assert outbox[0].subject == 'Confirm Your Email Address - Flask App'
            assert outbox[0].sender == 'leighmforrest@gmail.com'
            assert outbox[0].recipients[0] == 'rod@example.com'
            assert 'http://localhost/users/confirm/' in outbox[0].html

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
    
    def test_confirm_email_valid(self, client, db_test_user):
        confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = confirm_serializer.dumps(db_test_user.email, 'email-confirmation-salt')
        
        response = client.get(f"/users/confirm/{token}", follow_redirects=True)
        assert response.status_code == 200
        assert b"Thank you for confirming your email address!" in response.data
        
        query = db.select(User).where(User.email == db_test_user.email)
        user = db.session.execute(query).scalar_one()
        assert user.email_confirmed

    def test_email_already_confirmed(self, client, db_test_user ):
        confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = confirm_serializer.dumps(db_test_user.email, 'email-confirmation-salt')
        
        client.get(f"/users/confirm/{token}", follow_redirects=True)
        response = client.get(f"/users/confirm/{token}", follow_redirects=True)
        assert response.status_code == 200
        assert b"Account already confirmed." in response.data
        
        query = db.select(User).where(User.email == db_test_user.email)
        user = db.session.execute(query).scalar_one()
        assert user.email_confirmed
    
    def test_confirm_email_invalid(self, client, db_test_user):
        response = client.get('/users/confirm/bad_confirm_link', follow_redirects=True)
        assert response.status_code == 200
        assert b'The confirmation link is invalid or has expired.' in response.data
