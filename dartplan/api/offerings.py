from flask import g
from flask.ext.restful import Resource, fields, marshal, reqparse, inputs
from sqlalchemy.orm.exc import NoResultFound

from dartplan.database import db
from dartplan.login import login_required
from dartplan.models import User, Offering, Course, Term, Hour
from terms import term_fields
from courses import course_fields


class isEnrolled(fields.Raw):
    def output(self, key, offering):
        if not g.user:
            return False

        return offering in g.user.courses


class isUserAdded(fields.Raw):
    def output(self, key, offering):
        return True if offering.user_added == "Y" else False


class getName(fields.Raw):
    def output(self, key, offering):
        return str(offering)


class getHour(fields.Raw):
    def output(self, key, offering):
        return str(offering.hour)


class getEnrollment(fields.Raw):
    def output(self, key, offering):
        return User.query.filter(User.courses.contains(offering)).count()

offering_fields = {
    'id': fields.Integer,
    'name': getName,
    'term': fields.Nested(term_fields),
    'hour': getHour,
    'info': fields.String(attribute='desc'),
    'enrolled': isEnrolled,
    'user_added': isUserAdded,
    'enrollment': getEnrollment,
    'course': fields.Nested(course_fields)
}


class OfferingListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('course_id', type=int)
        self.reqparse.add_argument('term_id', type=int)
        super(OfferingListAPI, self).__init__()

    @login_required
    def get(self):
        return {'offerings': [marshal(offering, offering_fields)
                              for offering in g.user.courses.all()]}

    @login_required
    def post(self):
        args = self.reqparse.parse_args()

        course = Course.query.get_or_404(args.course_id)
        term = Term.query.get_or_404(args.term_id)

        offering = Offering.query.filter_by(course=course, term=term).first()

        if not offering:
            try:
                check_hour = Hour.query.filter_by(period="?").one()
            except NoResultFound:
                check_hour = Hour(period="?")
                db.session.add(check_hour)
                db.session.commit()

            offering = Offering(course_id=course.id, term_id=term.id,
                                hour_id=check_hour.id,
                                desc="***User Added***<br>Consult registrar for more info",
                                user_added="Y")

            db.session.add(offering)
            db.session.commit()

        if offering not in g.user.courses:
            g.user.courses.append(offering)
            db.session.commit()

        return {'offering': marshal(offering, offering_fields)}


class OfferingAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('enrolled', type=inputs.boolean)
        super(OfferingAPI, self).__init__()

    def get(self, id):
        offering = Offering.query.get_or_404(id)
        return {'offering': marshal(offering, offering_fields)}

    @login_required
    def put(self, id):
        args = self.reqparse.parse_args()

        offering = Offering.query.get_or_404(id)

        if args.enrolled is not None:
            if args.enrolled:
                if offering not in g.user.courses:
                    g.user.courses.append(offering)
            else:
                g.user.drop(offering)
            db.session.commit()

        return {'offering': marshal(offering, offering_fields)}


class CourseOfferingListAPI(Resource):
    def get(self, id):
        course = Course.query.get_or_404(id)
        offerings = Offering.query.filter_by(course=course).all()
        return {'offerings': [marshal(offering, offering_fields)
                              for offering in offerings]}
