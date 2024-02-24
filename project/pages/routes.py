from flask import current_app, render_template, redirect, flash, url_for, session, request

from . import pages_blueprint


@pages_blueprint.get("/")
def index():
    return render_template("pages/index.html")


@pages_blueprint.route("/message/write", methods=['GET','POST'])
def write_message():
    if request.method == "POST":
        for key, value in request.form.items():
            print(f"{key}: {value}")
        session["message"] = request.form.get("message")
        flash("Message updated.", "info")
        return redirect(url_for("pages.index"))
    return render_template("pages/add_message.html")


@pages_blueprint.get("/about")
def about():
    return render_template("pages/about.html")
