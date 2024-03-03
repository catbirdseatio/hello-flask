from threading import Thread
from flask import render_template, request, flash, redirect, url_for, copy_current_request_context, current_app
from flask_login import login_user, current_user, login_required, logout_user
from flask_mail import Message
from sqlalchemy.exc import IntegrityError

from project import db, mail
from project.models import User
from . import users_blueprint
from .forms import RegistrationForm, LoginForm

@users_blueprint.route("/register", methods=["POST", 'GET'])
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

            msg = Message(subject="Registration - Flask App",
                        body="THanks for registering with the Flask App",
                        recipients=[form.email.data])

            email_thread = Thread(target=send_email, args=[msg])
            email_thread.start()

            return redirect(url_for("users.login"))
        else:
            flash("Error in form data.", "danger")
    return render_template("users/registration.html", form=form)


@users_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in!")
        return redirect(url_for("pages.index"))
    form = LoginForm()

    if form.validate_on_submit():
        query = db.select(User).where(User.email == form.email.data)
        user = db.session.execute(query).scalar_one()        
        if user and user.is_password_correct(form.password.data):
            login_user(user)
            flash(f"Thanks for logging in, {current_user.email}", "success")
            return redirect(url_for("pages.index"))
        flash("Incorrect Login Credentials.", "danger")
    return render_template("users/login.html", form=form)


@users_blueprint.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("pages.index"))