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
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/dartplan.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('DartPlan Startup')

app.register_blueprint(flask_cas)

app.jinja_env.add_extension('jinja2.ext.loopcontrols')

db = SQLAlchemy(app)

from app import views, models