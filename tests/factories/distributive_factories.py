from tests.factories import *
from dartplan.models import Distributive
import factory.fuzzy


class DistributiveFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Distributive

    id = factory.Sequence(lambda n: n)
    abbr = factory.fuzzy.FuzzyChoice(["INT", "SOC", "NW", "QDS",
                                      "TMV", "TLA", "TAS"])
