from flask import Blueprint
from flask.ext.restful import Api

bp = Blueprint('api', __name__)
api = Api(bp, prefix="/api")

import offerings
