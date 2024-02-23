from flask import Flask, render_template, request, session, redirect, url_for
from markupsafe import escape

app = Flask(__name__)
app.secret_key = 'f36651d129c8b0eaa06a99a0afb87b1ffcb33386d8f93cf0e4c23697c9ab02db'


@app.get("/")
def index():
    return render_template("index.html")


@app.route("/message/write", methods=['GET','POST'])
def write_message():
    if request.method == "POST":
        for key, value in request.form.items():
            print(f"{key}: {value}")
        session["message"] = request.form.get("message")
        return redirect(url_for("index"))
    return render_template("add_message.html")


@app.route("/blog_posts/<int:post_id>")
def display_blog_post(post_id):
    return f"<h1>Blog Post #{post_id}...</h1>"


@app.get("/about")
def about():
    return "<h2>About this application...</h2>"
