import pytest
from tests.factories import user_factories, plan_factories


@pytest.fixture()
def user(db):
    user = user_factories.UserFactory()
    db.session.commit()
    return user


@pytest.fixture()
def user_with_two_plans(db):
    user = user_factories.UserFactory()
    plan_factories.PlanFactory(user=user)
    plan_factories.PlanFactory(user=user)
    db.session.commit()
    return user
