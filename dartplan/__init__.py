import os
from flask import Flask


def create_app(env=None):
    app = Flask(__name__, instance_relative_config=True,
                template_folder='frontend/templates',
                static_folder='frontend/static')

    # Load the default configuration
    app.config.from_object('config.default')

    # Load the configuration from the instance folder
    app.config.from_pyfile('config.py', silent=True)

    # Load the file specified by the APP_CONFIG_FILE environment variable
    # Variables defined here will override those in the default configuration
    env_config_file = os.environ.get('APP_CONFIG_FILE') or env

    if env_config_file:
        app.config.from_object('config.%s' % env_config_file)

    from dartplan.database import db
    db.init_app(app)

    from dartplan.mail import mail
    mail.init_app(app)

    from dartplan.login import flask_cas
    app.register_blueprint(flask_cas)

    from dartplan.frontend import frontend
    app.register_blueprint(frontend.bp)

    from dartplan.api import api
    app.register_blueprint(api.bp)

    from dartplan.admin import admin
    admin.init_app(app)

    app.jinja_env.add_extension('jinja2.ext.loopcontrols')

    return app
