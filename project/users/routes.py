from datetime import datetime
from threading import Thread
from flask import (
    render_template,
    request,
    flash,
    redirect,
    url_for,
    copy_current_request_context,
    current_app,
)
from flask_login import login_user, current_user, login_required, logout_user
import sqlalchemy as sa
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature
from flask_mail import Message

from project import db, mail
from project.models import User
from . import users_blueprint
from .forms import RegistrationForm, LoginForm, PasswordResetForm, PasswordForm


def generate_confirmation_email(user_email):
    confirmation_serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

    confirm_url = url_for(
        "users.confirm_email",
        token=confirmation_serializer.dumps(user_email, salt="email-confirmation-salt"),
        _external=True,
    )

    return Message(
        subject="Confirm Your Email Address - Flask App",
        html=render_template(
            "users/email/email_confirmation.html", confirm_url=confirm_url
        ),
        recipients=[user_email],
    )


def generate_password_reset_email(user_email):
    password_reset_serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

    password_reset_url = url_for(
        "users.process_password_reset",
        token=password_reset_serializer.dumps(
            user_email, salt="email-password_reset-salt"
        ),
        _external=True,
    )

    return Message(
        subject="Flask App - Password Reset Requested",
        html=render_template(
            "users/email/email_password_reset.html",
            password_reset_url=password_reset_url,
        ),
        recipients=[user_email],
    )


@users_blueprint.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()

    if request.method == "POST":
        if form.validate_on_submit():
            new_user = User(form.email.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash(f"Thanks for registering, {form.email.data}", "success")

            @copy_current_request_context
            def send_email(message):
                with current_app.app_context():
                    mail.send(message)

            msg = generate_confirmation_email(form.email.data)

            email_thread = Thread(target=send_email, args=[msg])
            email_thread.start()

            return redirect(url_for("users.login"))
        else:
            flash("Error in form data.", "danger")
    return render_template("users/registration.html", form=form)


@users_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in!")
        return redirect(url_for("pages.index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user is None or not user.is_password_correct(form.password.data):
            flash("Incorrect Login Credentials.", "danger")
            return redirect(url_for("users.login"))
        login_user(user)
        flash(f"Thanks for logging in, {current_user.email}", "success")
        return redirect(url_for("pages.index"))

    return render_template("users/login.html", form=form)


@users_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("pages.index"))


@users_blueprint.route("/confirm/<token>")
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        email = confirm_serializer.loads(
            token, salt="email-confirmation-salt", max_age=3600
        )
    except BadSignature:
        flash("The confirmation link is invalid or has expired.", "danger")
        return redirect(url_for("users.login"))

    query = db.select(User).where(User.email == email)
    user = db.session.execute(query).scalar_one()
    if user.email_confirmed:
        flash("Account already confirmed. Please login.", "info")
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("Thank you for confirming your email address!", "success")
    return redirect(url_for("pages.index"))


@users_blueprint.route("/password_reset", methods=["GET", "POST"])
def password_reset():
    form = PasswordResetForm()

    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))

        if user.email_confirmed:

            @copy_current_request_context
            def send_email(message):
                with current_app.app_context():
                    mail.send(message)

            msg = generate_password_reset_email(form.email.data)

            email_thread = Thread(target=send_email, args=[msg])
            email_thread.start()

            flash("Please check your email for a password reset link")
        else:
            flash("Your email must be confirmed before attempting a password reset.")
        return redirect(url_for("users.password_reset"))
    return render_template("users/password_reset.html", form=form)


@users_blueprint.route("/process_password_reset/<token>", methods=["GET", "POST"])
def process_password_reset(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        email = confirm_serializer.loads(
            token, salt="password-reset-salt", max_age=3600
        )
    except BadSignature:
        flash("The password reset link is invalid or has expired.", "danger")
        return redirect(url_for("users.login"))

    form = PasswordForm()

    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == email))

        if user is None:
            flash("Invalid email address.", "danger")
            return redirect(url_for("users.login"))

        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your password has been updated.")
        return redirect(url_for("users.login"))

    return render_template("/users/password_reset_with_token.html", form=form)
