from flask import Blueprint
v0 = Blueprint('v0', __name__)
from . import errors, views, forrms
