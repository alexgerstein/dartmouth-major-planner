from tests.factories import *
from dartplan.models import User, Plan


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User

    netid = factory.Sequence(lambda n: u'%d' % n)
    full_name = factory.Sequence(lambda n: u'User %d' % n)

    @factory.post_generation
    def grad_year(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.grad_year = extracted

            plan = self.plans.first()
            if not plan:
                plan = Plan(user_id=self.id)
                self.plans.append(plan)

            terms = self.get_all_terms()
            for term in terms:
                if term not in self.terms:
                    self.terms.append(term)

                if term not in plan.terms:
                    plan.terms.append(term)

    @factory.post_generation
    def offerings(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            plan = self.plans.first()
            if not plan:
                plan = Plan(user_id=self.id)
                self.plans.append(plan)

            for offering in extracted:
                if offering not in self.courses:
                    self.courses.append(offering)

                if offering not in plan.offerings:
                    plan.offerings.append(offering)
