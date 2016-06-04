import pytest
from dartplan.models import Plan


class TestPlan():

    def test_plan_reset_terms(self, plan):
        terms = plan.terms.all()
        assert len(terms) == 16
        assert terms[0].year == plan.user.grad_year - 4
        assert terms[0].season == 'F'

        plan.user.grad_year += 1
        plan.reset_terms()

        new_terms = plan.terms.all()
        assert len(new_terms) == 16
        assert new_terms[0] != terms[0]
        assert new_terms[-1].year == plan.user.grad_year
        assert new_terms[-1].season == 'X'

    def test_five_year_plan_reset_terms(self, five_year_plan):
        plan = five_year_plan
        terms = plan.terms.all()
        assert len(terms) == 20
        assert terms[0].year == plan.user.grad_year - 4
        assert terms[0].season == 'F'
        assert terms[-1].year == plan.user.grad_year + 1
        assert terms[-1].season == 'X'
