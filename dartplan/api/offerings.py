from flask import g
from flask.ext.restful import Resource, fields, marshal, reqparse, inputs

from dartplan.database import db
from dartplan.login import login_required
from dartplan.models import Offering, Course, Term, Hour


class isEnrolled(fields.Raw):
    def output(self, key, offering):
        if not g.user:
            return False

        return offering in g.user.courses

offering_fields = {
    'id': fields.Integer,
    'name': fields.String(attribute=lambda x: x),
    'hour': fields.String(attribute=lambda x: x.get_hour()),
    'possible_hours': fields.List(fields.String(attribute=lambda x: x.get_possible_hours())),
    'info': fields.String(attribute='desc'),
    'enrolled': isEnrolled
}


class OfferingListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('course_id', type=int)
        self.reqparse.add_argument('year', type=int)
        self.reqparse.add_argument('season', type=str)
        super(OfferingListAPI, self).__init__()

    @login_required
    def post(self):
        args = self.reqparse.parse_args()

        course = Course.query.get_or_404(args.course_id)
        term = Term.query.filter_by(year=args.year, season=args.season).first()

        offering = Offering.query.filter_by(course=course, term=term).first()

        if not offering:
            check_hour = Hour.query.filter_by(period="?").first()

            offering = Offering(course=course.id, term=term.id,
                                hour=check_hour.id,
                                desc="***User Added***<br>Consult registrar for more info",
                                user_added="Y")

            db.session.add(offering)
            db.session.commit()

        if offering in g.user.courses:
            return {"errors": {"enrolled": ["Already enrolled."]}}, 409
        else:
            g.user.take(offering)

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
                if offering in g.user.courses:
                    return {"errors": {"enrolled": ["Already enrolled."]}}, 409
                else:
                    g.user.take(offering)
            else:
                if offering not in g.user.courses:
                    return {"errors":
                            {"enrolled": ["Already not enrolled."]}}, 409
                else:
                    g.user.drop(offering)

        return {'offering': marshal(offering, offering_fields)}
