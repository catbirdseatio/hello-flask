from flask import render_template, request, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError

from project import db
from project.models import User
from . import users_blueprint
from .forms import RegistrationForm

@users_blueprint.route("/register", methods=["POST", 'GET'])
def register():
    form = RegistrationForm()

    if request.method == "POST":
        if form.validate_on_submit():
            try:
                new_user = User(form.email.data, form.password.data)
                db.session.add(new_user)
                db.session.commit()
                flash(f"Thanks for registering, {form.email.data}", "success")
                return redirect(url_for("pages.index"))
            except IntegrityError:
                db.session.rollback()
                flash(f"{form.email.data} already exists.", "warning")
        else:
            flash("Error in form data.", "danger")
    return render_template("users/registration.html", form=form)