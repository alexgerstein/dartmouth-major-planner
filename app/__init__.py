import os
from flask import Flask, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from flask_cas import flask_cas

app = Flask(__name__)
app.config.from_object('config')

app.register_blueprint(flask_cas)

db = SQLAlchemy(app)

from app import views, models