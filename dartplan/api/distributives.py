from flask.ext.restful import Resource, fields, marshal
from dartplan.login import login_required
from dartplan.models import Distributive

distributive_fields = {
    'id': fields.Integer,
    'abbr': fields.String
}


class DistributiveListAPI(Resource):
    @login_required
    def get(self):
        return {'distributives': [marshal(distrib, distributive_fields) for distrib in Distributive.query.order_by('abbr')]}
