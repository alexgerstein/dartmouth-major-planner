from flask_restful import Resource, marshal, fields, reqparse, inputs

from dartplan.authorization import plan_owned_by_user
from dartplan.login import login_required
from dartplan.models import Plan

from terms import term_fields
from offerings import offering_fields
from users import user_fields


class getPlanTerms(fields.Raw):
    def output(self, key, plan):
        terms = plan._get_all_terms()
        for term in terms:
            term.plan = plan
        return [marshal(term, term_fields) for term in terms]

plan_fields = {
    'title': fields.String,
    'terms': getPlanTerms,
    'offerings': fields.List(fields.Nested(offering_fields)),
    'fifth_year': fields.Boolean,
    'user': fields.Nested(user_fields)
}


class PlanAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('fifth_year', type=inputs.boolean)
        self.reqparse.add_argument('title')
        super(PlanAPI, self).__init__()

    def get(self, id):
        plan = Plan.query.get_or_404(id)
        return {'plan': marshal(plan, plan_fields)}

    @plan_owned_by_user
    @login_required
    def put(self, id):
        args = self.reqparse.parse_args()

        plan = Plan.query.get_or_404(id)

        if args.title:
            plan.rename(args.title)

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
