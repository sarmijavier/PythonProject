""" Initial configuration"""

#Flask
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

#Models
from .models import UserModel

#config
from .config import Config
from .auth import auth

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(email):
    return UserModel.query(email)


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    bootstrap = Bootstrap(app) 
    login_manager.init_app(app)
    app.config.from_object(Config)

    app.register_blueprint(auth)

    return app