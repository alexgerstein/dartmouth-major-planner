from flask import g, abort
from dartplan.models import Plan
from functools import wraps


# Wrapper function so no one can view someone else's plan
def plan_owned_by_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'plan_id' in kwargs:
            plan = Plan.query.get_or_404(kwargs['plan_id'])
        else:
            plan = Plan.query.get_or_404(kwargs['id'])

        if plan and g.user and plan.user_id != g.user.id:
            return abort(401)

        return fn(*args, **kwargs)
    return wrapper


# Wrapper function so no one can view someone else's plan
def is_pro_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if g.user and g.user.is_pro():
            return fn(*args, **kwargs)

        return abort(401)

    return wrapper
