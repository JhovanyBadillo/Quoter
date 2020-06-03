import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Conjunto de parámetros que se incluirán en app.config[]
    He encontrado que SEND_FILE_MAX_AGE_DEFAULT establece el tiempo
    de vida en la caché del navegador de los archivos estáticos, i.e.,
    los que están en la carpeta static (js, css, etc).
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER', default='smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', default='587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', default='true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SEND_FILE_MAX_AGE_DEFAULT = 5  # Sets Cache-Control header with max-age=30
    # PERMANENT_SESSION_LIFETIME = timedelta(seconds=900)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'postgres://'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'postgres://'

    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgres://'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
