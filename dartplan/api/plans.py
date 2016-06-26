from flask import g
from flask_restful import Resource, marshal, fields, reqparse, inputs

from dartplan.authorization import plan_owned_by_user, can_create_new_plan
from dartplan.login import login_required
from dartplan.models import Plan
from dartplan.database import db

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
    'id': fields.Integer,
    'title': fields.String,
    'fifth_year': fields.Boolean,
    'default': fields.Boolean,
    'user': fields.Nested(user_fields)
}

plan_detail_fields = {
    'terms': getPlanTerms,
    'offerings': fields.List(fields.Nested(offering_fields)),
}

plan_detail_fields = dict(plan_detail_fields, **plan_fields)


class PlanListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title')
        self.reqparse.add_argument('fifth_year', type=inputs.boolean)
        super(PlanListAPI, self).__init__()

    def get(self):
        return {'plans': [marshal(plan, plan_fields) for plan in g.user.plans]}

    @can_create_new_plan
    @login_required
    def post(self):
        args = self.reqparse.parse_args()

        default = g.user.plans.count() == 0
        plan = Plan(user=g.user, title=args.title,
                    fifth_year=args.fifth_year, default=default)
        db.session.add(plan)
        db.session.commit()

        plan.reset_terms()

        return {'plan': marshal(plan, plan_fields)}


class PlanAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('fifth_year', type=inputs.boolean)
        self.reqparse.add_argument('default', type=inputs.boolean)
        self.reqparse.add_argument('title')
        super(PlanAPI, self).__init__()

    def get(self, id):
        plan = Plan.query.get_or_404(id)
        return {'plan': marshal(plan, plan_detail_fields)}

    @plan_owned_by_user
    @login_required
    def put(self, id):
        args = self.reqparse.parse_args()

        plan = Plan.query.get_or_404(id)

        if args.title:
            plan.rename(args.title)

        if args.default is not None:
            if args.default and plan.default:
                return {"errors":
                        {"default": ["Plan already set as default."]}}, 409

            plan.set_as_default()

        if args.fifth_year is not None:
            if args.fifth_year and plan.fifth_year:
                return {"errors":
                        {"fifth_year": ["Plan already has 5th year."]}}, 409
            elif not args.fifth_year and not plan.fifth_year:
                return {"errors":
                        {"fifth_year":
                            ["Plan already excludes 5th year."]}}, 409

            plan.swap_fifth_year()

        return {'plan': marshal(plan, plan_detail_fields)}
