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

from flask import Flask, session, request, g, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from flask.ext.babel import Babel
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    babel = Babel(app)

    # initialize logging
    import logging.config
    logging.config.fileConfig(app.config['CONFIG_DIR'] + '/bonnie-flask.conf')

    # add main controller
    from views.root import root
    app.register_blueprint(root)

    # add (json) data controller
    from views.data import data
    app.register_blueprint(data)

    # add auth controller
    from auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    # add API controller
    from api import api
    app.register_blueprint(api, url_prefix='/api')

    # set locale from client headers
    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(['de','fr','en'])

    # render custom error pages
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def pagenotfound(e):
        return render_template('404.html'), 404

    return app

    