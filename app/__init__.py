import os
from flask import Flask, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from flask_cas import flask_cas

# __init__.py
# Alex Gerstein
# Initialize the Flask app according to config, views, and models

app = Flask(__name__)
app.config.from_object('config')

if not app.debug:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.ERROR)
    app.logger.info('DartPlan startup')

app.register_blueprint(flask_cas)

app.jinja_env.add_extension('jinja2.ext.loopcontrols')

# Redirect favicon
app.add_url_rule('/favicon.ico',
                 redirect_to=url_for('static', filename='favicon.ico'))

db = SQLAlchemy(app)

from app import views, models