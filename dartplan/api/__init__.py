from flask import Blueprint, g, session, redirect, url_for
from flask.ext.restful import Api

from dartplan.database import db
from dartplan.models import User

from offerings import OfferingAPI, OfferingListAPI
from courses import CourseAPI, CourseListAPI
from terms import TermAPI
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

            return (redirect(url_for('frontend.edit')))
    else:
        g.user = None


api.add_resource(OfferingListAPI, '/offerings', endpoint='offerings')
api.add_resource(OfferingAPI, '/offerings/<int:id>', endpoint='offering')
api.add_resource(CourseListAPI, '/courses', endpoint='courses')
api.add_resource(CourseAPI, '/courses/<int:id>', endpoint='course')
api.add_resource(TermAPI, '/terms/<int:id>', endpoint='term')
api.add_resource(UserAPI, '/user', endpoint='user')
