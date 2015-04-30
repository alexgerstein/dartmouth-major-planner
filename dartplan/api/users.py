from flask import g, redirect, url_for, session
from flask.ext.restful import Resource

from dartplan.login import login_required
from dartplan.database import db


class UserAPI(Resource):
    @login_required
    def delete(self):
        db.session.delete(g.user)
        db.session.commit()
        session.pop('user', None)
        return {'result': True}
