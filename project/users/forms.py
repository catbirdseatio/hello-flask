from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
import sqlalchemy as sa
from project import db
from project.models import User


EMAIL_LENGTH = {"min": 6, "max": 120}


class RegistrationForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(**EMAIL_LENGTH)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(**EMAIL_LENGTH)]
    )
    submit = SubmitField("Register")

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError(f"{email.data} already exists.")


class LoginForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(**EMAIL_LENGTH)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class PasswordResetForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(**EMAIL_LENGTH)]
    )
    submit = SubmitField("Login")

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is None:
            raise ValidationError("Invalid user address.")


class PasswordForm(FlaskForm):
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(**EMAIL_LENGTH)]
    )
    submit = SubmitField("Submit")
