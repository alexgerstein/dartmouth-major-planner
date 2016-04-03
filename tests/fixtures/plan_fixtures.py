import pytest
from tests.factories import plan_factories


@pytest.fixture()
def plan(request):
    return plan_factories.PlanFactory()
