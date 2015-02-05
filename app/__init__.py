from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.index'
login_manager.login_message = "You have to be logged in"


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api.v0 import v0 as api_v0_blueprint
    app.register_blueprint(api_v0_blueprint, url_prefix='/api/v0')

    from .users import allusers as users_users
    app.register_blueprint(users_users, url_prefix='/allusers')

    return app
