from flask.ext.restful import Resource, fields, marshal, reqparse, inputs
from dartplan.authorization import plan_owned_by_user
from dartplan.login import login_required
from dartplan.models import Plan, Term


class isOn(fields.Raw):
    def output(self, key, term):
        try:
            plan = term.plan
            return plan and term in plan.terms
        except AttributeError:
            return False


class getAbbr(fields.Raw):
    def output(self, key, term):
        return str(term)

term_fields = {
    'id': fields.Integer,
    'abbr': getAbbr,
    'on': isOn
}


class TermListAPI(Resource):
    @plan_owned_by_user
    @login_required
    def get(self, plan_id):
        plan = Plan.query.get_or_404(plan_id)
        terms = plan._get_all_terms()
        for term in terms:
            term.plan = plan

        return {'terms':
                [marshal(term, term_fields) for term in terms]}


class TermAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('on', type=inputs.boolean)
        super(TermAPI, self).__init__()

    @plan_owned_by_user
    @login_required
    def put(self, plan_id, id):
        args = self.reqparse.parse_args()

        term = Term.query.get_or_404(id)
        plan = Plan.query.get_or_404(plan_id)

        if args.on is not None:
            if args.on and term in plan.terms:
                return {"errors": {"on": ["Term is already marked on."]}}, 409
            elif not args.on and term not in plan.terms:
                return {"errors": {"on": ["Term is already marked off."]}}, 409

            plan.swap_onterm(term)

        term.plan = plan

        return {'term': marshal(term, term_fields)}
