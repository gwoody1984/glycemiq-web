from flask import Flask
from flask_login import LoginManager

from glycemiq_db import db
from glycemiq_web.config import config_as_obj

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config_as_obj('FLASK'))
    db.init_app(app)

    login_manager.session_protection = "strong"
    login_manager.login_view = "account.login"
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    from .account import account as account_blueprint
    app.register_blueprint(account_blueprint)

    from .portal import portal as portal_blueprint
    app.register_blueprint(portal_blueprint, url_prefix='/portal')

    return app
