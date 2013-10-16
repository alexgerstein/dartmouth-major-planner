import os
from flask import Flask, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from flask_cas import flask_cas

app = Flask(__name__)
app.config.from_object('config')

app.register_blueprint(flask_cas)

app.jinja_env.add_extension('jinja2.ext.loopcontrols')

db = SQLAlchemy(app)

from app import views, models