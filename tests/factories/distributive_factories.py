from tests.factories import *
from dartplan.models import Distributive


class DistributiveFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Distributive

    id = factory.Sequence(lambda n: n)
    abbr = factory.Iterator(["INT", "SOC", "NW", "QDS", "TMV", "TLA", "TAS"])
