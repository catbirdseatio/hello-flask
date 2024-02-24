from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from .extensions import db


class Message(db.Model):
    __tablename__ = 'messages'

    id = mapped_column(Integer(), primary_key=True)
    message = mapped_column(String(length=127))

    def __init__(self, message: str):
        self.message = message
    
    def __str__(self):
        return f"Message: {self.message}"