from flask import Blueprint

pages_blueprint = Blueprint("pages", __name__, template_folder="templates")

from . import routes