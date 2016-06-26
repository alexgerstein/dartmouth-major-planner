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


# Wrapper function so no only those on PRO or without a plan can
# create a new one
def can_create_new_plan(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if g.user:
            if g.user.is_pro() or (g.user.plans.count() == 0):
                return fn(*args, **kwargs)

        return abort(401)

    return wrapper
