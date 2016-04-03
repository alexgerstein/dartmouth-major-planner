from tests.factories import *
from dartplan.models import Plan
import factory.fuzzy


class PlanFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Plan

    grad_year = factory.fuzzy.FuzzyInteger(2015, 2020)
