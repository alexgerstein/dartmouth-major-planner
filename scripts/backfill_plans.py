from dartplan.database import db
from dartplan.models import User, Plan


def run_backfill():
    for user in User.query.all():
        plan = user.plans.first()

        if plan:
            continue
        else:
            plan = Plan(user_id=user.id)
            db.session.add(plan)
            db.session.commit()

            for course in user.courses:
                plan.enroll(course)

            for term in user.terms:
                if term not in plan.terms:
                    plan.terms.append(term)
                    db.session.commit()
