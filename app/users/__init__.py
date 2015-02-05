from flask import Blueprint
allusers = Blueprint('allusers', __name__)
from . import errors, views