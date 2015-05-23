from tests.factories import *
from dartplan.models import Hour


class HourFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Hour

    id = factory.Sequence(lambda n: n)
    period = factory.Sequence(lambda n: u'%d:00 PM' % n)
