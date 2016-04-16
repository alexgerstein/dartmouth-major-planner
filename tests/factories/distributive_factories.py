from tests.factories import *
from dartplan.models import Distributive
import factory.fuzzy


class DistributiveFactory(BaseFactory):
    class Meta:
        model = Distributive

    abbr = factory.fuzzy.FuzzyChoice(["INT", "SOC", "NW", "QDS",
                                      "TMV", "TLA", "TAS"])
