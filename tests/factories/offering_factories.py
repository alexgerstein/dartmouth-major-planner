from tests.factories import *
from dartplan.models import Offering
from term_factories import TermFactory
from hour_factories import HourFactory
import factory.fuzzy

class OfferingFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Offering

    id = factory.Sequence(lambda n: n)

    term = factory.SubFactory(TermFactory)
    hour = factory.SubFactory(HourFactory)
    desc = factory.Sequence(lambda n: "Course %d covers stuff..." % n)

    median = factory.fuzzy.FuzzyChoice(['A', 'B', 'C', 'D'])

    added = factory.Iterator(['F'])
    user_added = factory.fuzzy.FuzzyChoice(['Y', 'N'])

    @factory.post_generation
    def distributives(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for distrib in extracted:
                self.distributives.append(distrib)
