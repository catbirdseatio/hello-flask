from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, validates
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db


class Message(db.Model):
    __tablename__ = 'messages'

    id = mapped_column(Integer(), primary_key=True)
    message = mapped_column(String(length=127))

    def __init__(self, message: str):
        self.message = message
    
    def __str__(self):
        return f"Message: {self.message}"


class User(db.Model):
    __tablename__ = 'users'

    id = mapped_column(Integer(), primary_key=True)
    email = mapped_column(String(), unique=True)
    password_hashed = mapped_column(String(128))

    def __init__(self, email: str, password_plaintext: str):
        self.email = email 
        self.password_hashed = self._generate_password_hash(password_plaintext)
    
    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)
    
    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def __str__(self):
        return f"<User: {self.email}>"