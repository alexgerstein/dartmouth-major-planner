import pytest
from dartplan.models import Plan


class TestPlan():

    def test_plan_reset_terms(self, plan):
        assert plan.terms.count() == 16
        initial_term = plan.terms.first()
        plan.user.grad_year += 1
        plan.reset_terms()
        assert plan.terms.count() == 16
        assert plan.terms.first() != initial_term
