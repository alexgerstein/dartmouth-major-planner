from tests.factories import *
from dartplan.models import Offering
from term_factories import TermFactory
from hour_factories import HourFactory


class OfferingFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Offering

    id = factory.Sequence(lambda n: n)

    term = factory.SubFactory(TermFactory)
    hour = factory.SubFactory(HourFactory)
    desc = factory.Sequence(lambda n: "Course %d covers stuff..." % n)

    median = factory.Iterator(['A', 'B', 'C', 'D'])

    added = factory.Iterator(['F'])
    user_added = factory.Iterator(['Y', 'N'])
