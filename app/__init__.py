from flask import Flask, session, g, render_template
from flask.ext.bootstrap import Bootstrap
from config import config

bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)

    # initialize logging
    import logging.config
    logging.config.fileConfig(app.config['CONFIG_DIR'] + '/bonnie-flask.conf')

    # add main controller
    from views.root import root
    app.register_blueprint(root)

    # add API controller
    from api import api
    app.register_blueprint(api, url_prefix='/api')

    return app
