from flask import Flask
from glycemiq_db import db

from glycemiq_web.config import config_as_obj


def create_app():
    app = Flask(__name__)
    app.config.from_object(config_as_obj('FLASK'))
    db.init_app(app)

    from .account import account as account_blueprint
    app.register_blueprint(account_blueprint)

    return app