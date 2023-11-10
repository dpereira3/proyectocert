from flask import Blueprint

curso_bp = Blueprint('curso', __name__, template_folder='templates')

from . import routes