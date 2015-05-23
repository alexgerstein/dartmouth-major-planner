from tests.factories import *
from dartplan.models import Term
import factory.fuzzy


class TermFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Term

    id = factory.Sequence(lambda n: n)
    year = factory.fuzzy.FuzzyInteger(2015, 2020)
    season = factory.fuzzy.FuzzyChoice(['F', 'W', 'S', 'X'])
