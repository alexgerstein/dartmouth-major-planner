from tests.factories import *
from dartplan.models import User
from dartplan.frontend.frontend import generate_terms


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
            terms = generate_terms(extracted)
            for term in terms:
                if term not in self.terms:
                    self.terms.append(term)

    @factory.post_generation
    def offerings(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for offering in extracted:
                if offering not in self.courses:
                    self.courses.append(offering)
