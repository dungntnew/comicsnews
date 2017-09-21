from comicnews.data.models import db, Role, User
from flask_compress import Compress
from flask_security import Security, SQLAlchemyUserDatastore
import os
import logging


class BaseConfig(object):
    DEBUG = False
    TESTING = False

    JSON_SORT_KEYS: False
    THREADS_PER_PAGE: 2

    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_ECHO: False
    SQLALCHEMY_TRACK_MODIFICATIONS: True
    DATABASE_CONNECT_OPTIONS: {}

    CSRF_ENABLED: True
    CSRF_SESSION_KEY: '1d94e52c-1c89-4515-b87a-f48cf3cb7f0b'
    SECRET_KEY = '1d94e52c-1c89-4515-b87a-f48cf3cb7f0b'

    BASIC_AUTH_USER: 'admin'
    BASIC_AUTH_PASSWORD: 'admin'
    DEFAULT_ADMIN_EMAIL: 'admin@gmail.com'
    DEFAULT_ADMIN_PASSWORD: 'abcd1234'
    TOKEN_EXP: 31536000

    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'comicnews.log'
    LOGGING_LEVEL = logging.DEBUG

    SECURITY_CONFIRMABLE = False
    CACHE_TYPE = 'simple'
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500
    SUPPORTED_LANGUAGES = {'en': 'English', 'ja': 'Japanese'}

    BABEL_DEFAULT_LOCALE = 'ja'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///comicnews.db'
    SECRET_KEY = 'a9eec0e0-23b7-4788-9a92-318347b9a39f'


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql://manga:manga@evuedev.cigku9rtjcia.us-west-2.rds.amazonaws.com/manga?charset=utf8'
    SECRET_KEY = 'a9eec0e0-23b7-4788-9a92-318347b9a39f'


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = '792842bc-c4df-4de1-9177-d5207bd9faa6'


config = {
    "development": "comicnews.config.DevelopmentConfig",
    "production": "comicnews.config.ProductionConfig",
    "testing": "comicnews.config.TestingConfig",
    "default": "comicnews.config.DevelopmentConfig"
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)
    # Configure logging
    handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    # Configure Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)
    # Configure Compressing
    Compress(app)
