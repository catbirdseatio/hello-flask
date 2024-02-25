from project.models import Message


def test_new_message(message):
    assert message.message == "Hello Python!"


def test___str__(message):
    assert str(message) == "Message: Hello Python!"
