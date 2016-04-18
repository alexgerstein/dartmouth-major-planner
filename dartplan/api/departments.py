from flask.ext.restful import Resource, fields, marshal
from dartplan.login import login_required
from dartplan.models import Department

department_fields = {
    'id': fields.Integer,
    'abbr': fields.String
}


class DepartmentListAPI(Resource):
    @login_required
    def get(self):
        return {'departments': [marshal(dept, department_fields) for dept in Department.query.order_by('abbr')]}
