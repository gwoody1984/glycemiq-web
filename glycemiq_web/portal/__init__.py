from flask import Blueprint
from flask_login import login_required

portal = Blueprint('portal', __name__ ,template_folder='templates')

@portal.before_request
@login_required
def ensure_logged_in():
    pass

from . import views