from flask import current_app, render_template, redirect, flash, url_for, session, request, abort

from . import pages_blueprint
from ..models import Message, db


@pages_blueprint.get("/")
def index():
    query = db.select(Message).order_by(Message.id.desc())
    message = db.session.execute(query).scalars().first()
    print(message)
    return render_template("pages/index.html", message=message)


@pages_blueprint.route("/message/write", methods=['GET','POST'])
def write_message():
    if request.method == "POST":
        try:
            message = request.form.get("message")
            new_message = Message(message=message)
            db.session.add(new_message)
            db.session.commit()
            flash("Message updated.", "info")
            return redirect(url_for("pages.index"))
        except Exception as e:
            flash(e, "danger")
    return render_template("pages/add_message.html")


@pages_blueprint.get("/about")
def about():
    return render_template("pages/about.html")

@pages_blueprint.get("/admin")
def admin():
    abort(403)
