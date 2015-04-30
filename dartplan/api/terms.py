from flask import g
from flask.ext.restful import Resource, fields, marshal, reqparse, inputs
from dartplan.login import login_required
from dartplan.models import Term

term_fields = {
    'year': fields.Integer,
    'season': fields.String,
    'on': fields.Boolean(attribute=lambda x: x in g.user.terms)
}


class TermAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('on', type=inputs.boolean)
        super(TermAPI, self).__init__()

    @login_required
    def put(self, id):
        args = self.reqparse.parse_args()

        term = Term.query.get_or_404(id)

        if args.on is not None:
            if args.on and term in g.user.terms:
                return {"errors": {"on": ["Term is already marked on."]}}, 409
            elif not args.on and term not in g.user.terms:
                return {"errors": {"on": ["Term is already marked off."]}}, 409

            g.user.swap_onterm(term)

        return {'term': marshal(term, term_fields)}
