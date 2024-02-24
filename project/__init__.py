import os
from flask import Flask
from dotenv import load_dotenv


load_dotenv()


def register_blueprints(app):
    from project.pages import pages_blueprint

    app.register_blueprint(pages_blueprint, url_prefix="/")


# Application Factory Pattern
def create_app():
    app = Flask(__name__)
    config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")
    app.config.from_object(config_type)

    register_blueprints(app)

    return app
