from flask import g, session
from flask_restful import Resource, marshal, fields

from dartplan.login import login_required
from dartplan.database import db


class getEmail(fields.Raw):
    def output(self, key, user):
        return user.email()


class getIsPro(fields.Raw):
    def output(self, key, user):
        return user.is_pro()


class getNumberOfPlans(fields.Raw):
    def output(self, key, user):
        return user.plans.count()

user_fields = {
    'id': fields.Integer,
    'nickname': fields.String,
    'netid': fields.String,
    'email': getEmail,
    'grad_year': fields.Integer,
    'email_course_updates': fields.Boolean,
    'email_Dartplan_updates': fields.Boolean,
    'is_pro': getIsPro,
    'number_of_plans': getNumberOfPlans
}


class UserAPI(Resource):
    @login_required
    def get(self):
        return {'user': marshal(g.user, user_fields)}

    @login_required
    def delete(self):
        db.session.delete(g.user)
        db.session.commit()
        session.pop('user', None)
        return {'result': True}
