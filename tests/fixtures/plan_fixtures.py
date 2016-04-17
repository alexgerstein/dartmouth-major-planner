import pytest
from dartplan.models import Term
from tests.factories import plan_factories, offering_factories


@pytest.fixture()
def plan(db):
    plan = plan_factories.PlanFactory()
    db.session.commit()
    return plan


@pytest.fixture()
def plan_with_offering(db):
    plan = plan_factories.PlanFactory()
    term = Term.query.filter_by(year=plan.user.grad_year - 1).first()
    offering = offering_factories.OfferingFactory(term=term)
    plan.offerings.append(offering)
    db.session.commit()
    return plan


@pytest.fixture()
def plan_with_user_added_offering(db, user_added_offering):
    plan = plan_factories.PlanFactory(offerings=[user_added_offering])
    db.session.commit()
    return plan
