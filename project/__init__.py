import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from .models import Message
from .extensions import db, db_migration


load_dotenv()


def register_blueprints(app):
    from project.pages import pages_blueprint
    from project.users import users_blueprint

    app.register_blueprint(pages_blueprint, url_prefix="/")
    app.register_blueprint(users_blueprint, url_prefix="/users")


def register_error_pages(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template("405.html"), 405

    @app.errorhandler(403)
    def not_permitted(e):
        return render_template("403.html"), 403

    @app.errorhandler(500)
    def page_not_found(e):
        return render_template("500.html"), 500


def initialize_extensions(app):
    db.init_app(app)
    db_migration.init_app(app, db)


# Application Factory Pattern
def create_app():
    app = Flask(__name__)
    config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")
    app.config.from_object(config_type)

    initialize_extensions(app)
    register_blueprints(app)
    register_error_pages(app)

    # shell context
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db, "Message": Message}

    return app
