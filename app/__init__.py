from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from config import config

mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()

login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .clients import clients as clients_blueprint
    from .products import products as products_blueprint
    from .quotations import quotations as quotations_blueprint
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(clients_blueprint, url_prefix='/clientes')
    app.register_blueprint(products_blueprint, url_prefix='/productos')
    app.register_blueprint(quotations_blueprint, url_prefix='/cotizaciones')

    return app

