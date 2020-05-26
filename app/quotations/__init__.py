from flask import Blueprint

quotations = Blueprint('quotations', __name__)

from . import views