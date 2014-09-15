import os
from ConfigParser import SafeConfigParser

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-secret'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    CONFIG_DIR = os.path.join(basedir, 'config')
    CONFIG_FILE = os.path.join(basedir, 'config', 'bonnie-flask.conf')
    DATA_DIR = os.path.join(basedir, 'data')

    def __init__(self):
        parser = SafeConfigParser()
        parser.read(self.CONFIG_FILE)

        if parser.has_section('db') and parser.has_option('db', 'uri'):
            self.SQLALCHEMY_DATABASE_URI = parser.get('db', 'uri')

    def init_app(self, app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.db')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.db')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.db')


config = {
    'development': DevelopmentConfig(),
    'testing': TestingConfig(),
    'production': ProductionConfig(),
    'default': DevelopmentConfig()
}