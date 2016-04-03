from flask.ext.restful import Resource, marshal, fields

from dartplan.login import login_required
from dartplan.models import Plan

from terms import term_fields
from offerings import offering_fields

plan_fields = {
    'title': fields.String,
    'terms': fields.List(fields.Nested(term_fields)),
    'offerings': fields.List(fields.Nested(offering_fields))
}


class PlanAPI(Resource):
    @login_required
    def get(self, id):
        plan = Plan.query.get_or_404(id)
        return {'plan': marshal(plan, plan_fields)}
