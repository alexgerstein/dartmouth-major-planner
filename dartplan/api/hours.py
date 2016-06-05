from flask.ext.restful import Resource, fields, marshal
from dartplan.login import login_required
from dartplan.models import Hour

hour_fields = {
    'id': fields.Integer,
    'period': fields.String
}


class HourListAPI(Resource):
    def get(self):
        return {'hours': [marshal(hour, hour_fields) for hour in Hour.query.order_by('id')]}
