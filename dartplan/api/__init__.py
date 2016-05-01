from flask import Blueprint, g, session, redirect, url_for
from flask.ext.restful import Api, abort
from functools import wraps

from dartplan.database import db
from dartplan.models import User, Plan

from offerings import (OfferingAPI, OfferingListAPI,
                       CourseOfferingListAPI)
from courses import CourseAPI, CourseListAPI
from terms import TermAPI, TermListAPI
from hours import HourListAPI
from departments import DepartmentListAPI
from distributives import DistributiveListAPI
from medians import MedianListAPI
from plans import PlanAPI
from users import UserAPI

bp = Blueprint('api', __name__)
api = Api(bp, prefix="/api")


# Always track if there is a current user signed in
# If unrecognized user is in, add them to user database
@bp.before_request
def fetch_user():

    if 'user' in session:
        g.user = User.query.filter_by(netid=session['user']['netid']).first()
        if g.user is None:
            g.user = User(session['user']['name'], session['user']['netid'])
            db.session.add(g.user)
            db.session.commit()

            plan = Plan(user_id=g.user.id)
            db.session.add(plan)
            db.session.commit()

            return (redirect(url_for('frontend.edit')))
    else:
        g.user = None


api.add_resource(OfferingListAPI, '/plans/<int:plan_id>/offerings',
                 endpoint='offerings')
api.add_resource(OfferingAPI, '/plans/<int:plan_id>/offerings/<int:id>',
                 endpoint='offering')
api.add_resource(CourseListAPI, '/courses', endpoint='courses')
api.add_resource(CourseAPI, '/courses/<int:id>', endpoint='course')
api.add_resource(CourseOfferingListAPI, '/courses/<int:id>/offerings',
                 endpoint='course_offerings')
api.add_resource(DistributiveListAPI, '/distributives',
                 endpoint='distributives')
api.add_resource(DepartmentListAPI, '/departments', endpoint='departments')
api.add_resource(HourListAPI, '/hours', endpoint='hours')
api.add_resource(MedianListAPI, '/medians', endpoint='medians')
api.add_resource(TermListAPI, '/plans/<int:plan_id>/terms', endpoint='terms')
api.add_resource(TermAPI, '/plans/<int:plan_id>/terms/<int:id>',
                 endpoint='term')
api.add_resource(PlanAPI, '/plans/<int:id>', endpoint='plan')
api.add_resource(UserAPI, '/user', endpoint='user')
