from tests.factories import *
from dartplan.models import User

import factory.fuzzy


class UserFactory(BaseFactory):
    class Meta:
        model = User

    netid = factory.Sequence(lambda n: u'%d' % n)
    full_name = factory.Sequence(lambda n: u'User %d' % n)
    grad_year = factory.fuzzy.FuzzyInteger(2015, 2020)
    amount_paid = 0
