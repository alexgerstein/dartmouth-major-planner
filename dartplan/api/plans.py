from flask import g
from flask.ext.restful import Resource, marshal, fields

from dartplan.login import login_required

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
    def get(self):
        return {'plan': marshal(g.user.plans.first(), plan_fields)}
