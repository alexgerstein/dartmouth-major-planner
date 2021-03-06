from flask_restful import Resource, fields, marshal
from dartplan.login import login_required
from dartplan.models import Department

department_fields = {
    'id': fields.Integer,
    'abbr': fields.String
}


class DepartmentListAPI(Resource):
    def get(self):
        return {'departments': [marshal(dept, department_fields) for dept in Department.query.order_by('abbr')]}
