from tests.factories import *
from dartplan.models import Department


class DepartmentFactory(BaseFactory):
    class Meta:
        model = Department

    name = factory.Sequence(lambda n: "Department %d" % n)
    abbr = factory.Sequence(lambda n: "D%d" % n)
