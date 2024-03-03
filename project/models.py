from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.orm import mapped_column, validates
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login

from .extensions import db


class Message(db.Model):
    __tablename__ = "messages"

    id = mapped_column(Integer(), primary_key=True)
    message = mapped_column(String(length=127))

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"Message: {self.message}"


class User(flask_login.UserMixin, db.Model):
    __tablename__ = "users"

    id = mapped_column(Integer(), primary_key=True)
    email = mapped_column(String(), unique=True)
    password_hashed = mapped_column(String(128))
    registered_on = mapped_column(DateTime())
    email_confirmation_sent_on = mapped_column(DateTime())
    email_confirmed = mapped_column(Boolean(), default=False)
    email_confirmed_on = mapped_column(DateTime())

    def __init__(self, email: str, password_plaintext: str):
        self.email = email
        self.password_hashed = self._generate_password_hash(password_plaintext)
        self.registered_on = datetime.now()
        self.email_confirmation_sent_on = datetime.now()
        self.email_confirmed = False
        self.email_confirmed_on = None

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def __str__(self):
        return f"<User: {self.email}>"
