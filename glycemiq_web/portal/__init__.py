from flask import Blueprint

portal = Blueprint('portal', __name__ ,template_folder='templates')

from . import views