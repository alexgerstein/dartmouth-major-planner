from flask_restful import Resource, fields, marshal, reqparse

from dartplan.models import Course, Offering, Department, Distributive

MEDIANS = ['A', 'A/A-', 'A-', 'A-/B+', 'B+', 'B+/B', 'B', 'B/B-',
           'B-', 'B-/C+', 'C+', 'C+/C', 'C']


class getFullName(fields.Raw):
    def output(self, key, course):
        return str(course)

course_fields = {
    'id': fields.Integer,
    'number': fields.Float,
    'name': fields.String,
    'full_name': getFullName
}


class CourseListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('dept_id', type=int)
        self.reqparse.add_argument('term_id', type=int)
        self.reqparse.add_argument('hour_id', type=int)
        self.reqparse.add_argument('distrib_id', type=int)
        self.reqparse.add_argument('median_id', type=int)
        super(CourseListAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()

        courses = Course.query.join(Offering)

        if args.dept_id:
            courses = courses.filter(Course.department_id == args.dept_id)

        if args.term_id:
            courses = courses.filter(Offering.term_id == args.term_id)

        if args.hour_id:
            courses = courses.filter(Offering.hour_id == args.hour_id)

        if args.distrib_id:
            distrib = Distributive.query.filter_by(id=args.distrib_id).first()
            courses = courses.filter(Offering.distributives.contains(distrib))

        if args.median_id:
            courses = courses.filter(Course.avg_median
                                           .in_(MEDIANS[:args.median_id + 1]))

        courses = courses.join(Department).order_by('abbr', 'number').all()

        return {'courses': [marshal(course, course_fields)
                            for course in courses]}


class CourseAPI(Resource):
    def get(self, id):
        course = Course.query.get_or_404(id)
        return {'course': marshal(course, course_fields)}
