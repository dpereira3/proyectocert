from flask import Blueprint
#from app.curso.models import Curso


curso_bp = Blueprint('curso', __name__, template_folder='templates')

from . import routes
