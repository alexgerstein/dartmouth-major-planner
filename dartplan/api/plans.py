from flask import g
from flask.ext.restful import Resource, marshal, fields

from dartplan.login import login_required
from dartplan.models import Plan

from terms import term_fields
from offerings import offering_fields


class getPlanTerms(fields.Raw):
    def output(self, key, plan):
        return [marshal(term, term_fields) for term in plan._get_all_terms()]

plan_fields = {
    'title': fields.String,
    'terms': getPlanTerms,
    'offerings': fields.List(fields.Nested(offering_fields))
}


class PlanAPI(Resource):
    @login_required
    def get(self, id):
        plan = Plan.query.get_or_404(id)
        return {'plan': marshal(plan, plan_fields)}
