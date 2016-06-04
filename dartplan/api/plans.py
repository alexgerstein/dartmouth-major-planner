from flask.ext.restful import Resource, marshal, fields, reqparse, inputs

from dartplan.authorization import plan_owned_by_user
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
    'offerings': fields.List(fields.Nested(offering_fields)),
    'fifth_year': fields.Boolean
}


class PlanAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('fifth_year', type=inputs.boolean)
        super(PlanAPI, self).__init__()

    @plan_owned_by_user
    @login_required
    def get(self, id):
        plan = Plan.query.get_or_404(id)
        return {'plan': marshal(plan, plan_fields)}

    @plan_owned_by_user
    @login_required
    def put(self, id):
        args = self.reqparse.parse_args()

        plan = Plan.query.get_or_404(id)

        if args.fifth_year is not None:
            if args.fifth_year and plan.fifth_year:
                return {"errors":
                        {"fifth_year": ["Plan already has 5th year."]}}, 409
            elif not args.fifth_year and not plan.fifth_year:
                return {"errors":
                        {"fifth_year":
                            ["Plan already excludes 5th year."]}}, 409

            plan.swap_fifth_year()

        return {'plan': marshal(plan, plan_fields)}
