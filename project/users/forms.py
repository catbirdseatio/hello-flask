from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
import sqlalchemy as sa
from project import db
from project.models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email(), Length(min=6, max=120)
    ])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=5, max=40)])
    submit = SubmitField("Register")

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError(f"{email.data} already exists.")