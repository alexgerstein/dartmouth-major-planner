from tests.factories import *
from dartplan.models import Plan

from user_factories import UserFactory


class PlanFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Plan

    user = factory.SubFactory(UserFactory)
