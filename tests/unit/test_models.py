from project.models import Message


def test_new_message(message):
    assert message.message == "Hello Python!"


def test___str__(message):
    assert str(message) == "Message: Hello Python!"

def test_set_password(new_user):
    new_user.set_password('FlaskIsStillAwesome456')
    assert new_user.email == "roderick@email.com"
    assert new_user.password_hashed != 'FlaskIsStillAwesome456'
    assert new_user.is_password_correct('FlaskIsStillAwesome456')