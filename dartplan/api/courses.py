from collections import Counter
from flask.ext.restful import Resource, fields, marshal, reqparse

from dartplan.models import Course, Offering, Department, Distributive

MEDIANS = ['A', 'A/A-', 'A-', 'A-/B+', 'B+', 'B+/B', 'B', 'B/B-',
           'B-', 'B-/C+', 'C+', 'C+/C', 'C']

term_fields = {
    'term': fields.String,
    'enrolled': fields.Integer
}

course_fields = {
    'id': fields.Integer,
    'number': fields.Float,
    'name': fields.String,
    'full_name': fields.String(attribute=lambda x: x)
}

course_detail_fields = {
    'terms': fields.List(fields.Nested(term_fields)),
    'user_terms': fields.List(fields.Nested(term_fields))
}
course_detail_fields = dict(course_fields, **course_detail_fields)


class CourseListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('department_id', type=int)
        self.reqparse.add_argument('term_id', type=int)
        self.reqparse.add_argument('hour_id', type=int)
        self.reqparse.add_argument('distrib_id', type=int)
        self.reqparse.add_argument('median_id', type=int)
        super(CourseListAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()

        courses = Course.query.join(Offering)

        if args.department_id:
            courses = courses.filter(Course.department_id == args.department_id)

        if args.term_id:
            courses = courses.filter(Offering.term_id == args.term_id)

        if args.hour_id:
            courses = courses.filter(Offering.hour_id == args.hour_id)

        if args.distrib_id:
            distrib = Distributive.query.filter_by(id=args.distrib_id).first()
            courses = courses.filter(Offering.distributives.contains(distrib))

        if args.median_id:
            courses = courses.filter(Course.avg_median.in_(MEDIANS[:args.median_id + 1]))

        courses = courses.join(Department).order_by('abbr', 'number').all()

        return {'courses': [marshal(course, course_fields)
                            for course in courses]}


class CourseAPI(Resource):
    def get(self, id):
        course = Course.query.get_or_404(id)

        available_user_offerings = Offering.query.filter_by(course=course, user_added="Y").all()
        available_registrar_offerings = Offering.query.filter_by(course=course, user_added="N").all()

        enrolled_counter = Counter()
        for offering in available_registrar_offerings:
            enrolled_counter.update({offering.term: offering.get_user_count()})

        course.terms = [{'term': term, 'enrolled': enrolled}
                        for term, enrolled in enrolled_counter]

        enrolled_counter = Counter()
        for offering in available_user_offerings:
            enrolled_counter.update({offering.term: offering.get_user_count()})

        course.user_terms = [{'term': term, 'enrolled': enrolled}
                             for term, enrolled in enrolled_counter]

        return {'course': marshal(course, course_detail_fields)}
