from tests.factories import *
from dartplan.models import Hour


class HourFactory(BaseFactory):
    class Meta:
        model = Hour

    period = factory.Sequence(lambda n: u'%d:00 PM' % n)
