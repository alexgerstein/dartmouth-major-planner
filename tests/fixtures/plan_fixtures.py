import pytest
from tests.factories import plan_factories


@pytest.fixture()
def plan(db):
    plan = plan_factories.PlanFactory()
    db.session.commit()
    return plan


@pytest.fixture()
def plan_with_offering(db, offering):
    plan = plan_factories.PlanFactory(offerings=[offering])
    db.session.commit()
    return plan


@pytest.fixture()
def plan_with_user_added_offering(db, user_added_offering):
    plan = plan_factories.PlanFactory(offerings=[user_added_offering])
    db.session.commit()
    return plan
