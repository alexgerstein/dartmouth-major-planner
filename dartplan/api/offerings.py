from flask import g
from flask_restful import Resource, fields, marshal, reqparse, inputs
from sqlalchemy.orm.exc import NoResultFound

from dartplan.authorization import plan_owned_by_user
from dartplan.database import db
from dartplan.login import login_required
from dartplan.models import Plan, Offering, Course, Term, Hour
from terms import term_fields
from courses import course_fields


class isEnrolled(fields.Raw):
    def output(self, key, offering):
        try:
            plan = offering.plan
            return plan and offering in plan.offerings
        except AttributeError:
            return False


class isUserAdded(fields.Raw):
    def output(self, key, offering):
        return offering.user_added == "Y"


class getName(fields.Raw):
    def output(self, key, offering):
        return str(offering)


class getHour(fields.Raw):
    def output(self, key, offering):
        return str(offering.hour)


class getEnrollment(fields.Raw):
    def output(self, key, offering):
        return Plan.query.filter(Plan.offerings.contains(offering)).count()

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

    @plan_owned_by_user
    @login_required
    def post(self, plan_id):
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

        plan = Plan.query.get_or_404(plan_id)
        if plan:
            plan.enroll(offering)

        return {'offering': marshal(offering, offering_fields)}


class OfferingAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('enrolled', type=inputs.boolean)
        super(OfferingAPI, self).__init__()

    @plan_owned_by_user
    @login_required
    def put(self, plan_id, id):
        args = self.reqparse.parse_args()

        offering = Offering.query.get_or_404(id)
        plan = Plan.query.get_or_404(plan_id)

        if args.enrolled is not None:
            if args.enrolled:
                plan.enroll(offering)
                offering.plan = plan
            else:
                if plan.drop(offering):
                    return {'offering': None}
        return {'offering': marshal(offering, offering_fields)}


class CourseOfferingListAPI(Resource):
    def get(self, plan_id, course_id):
        course = Course.query.get_or_404(course_id)
        plan = Plan.query.get_or_404(plan_id)
        offerings = Offering.query.filter_by(course=course).all()

        for offering in offerings:
            offering.plan = plan

        return {'offerings': [marshal(offering, offering_fields)
                              for offering in offerings]}
