# -*- coding: utf-8 -*-
#
# Copyright 2014 Kolab Systems AG (http://www.kolabsys.com)
#
# Thomas Bruederli <bruederli at kolabsys.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

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
    BABEL_DEFAULT_LOCALE = 'en_US'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    BOOTSTRAP_SERVE_LOCAL = True
    BOOTSTRAP_USE_MINIFIED = False

    def __init__(self):
        parser = SafeConfigParser()
        parser.read(self.CONFIG_FILE)

        if parser.has_section('db') and parser.has_option('db', 'uri'):
            self.SQLALCHEMY_DATABASE_URI = self.parser.get('db', 'uri')

        self.STORAGE = dict()
        if parser.has_section('storage'):
            for key,val in parser.items('storage'):
                self.STORAGE[key] = val

        self.API = dict()
        if parser.has_section('api'):
            for key,val in parser.items('api'):
                self.API[key] = val

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