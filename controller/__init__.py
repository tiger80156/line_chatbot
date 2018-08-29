from flask import Blueprint
blueprint = Blueprint('views', __name__)

from . import flask_api
