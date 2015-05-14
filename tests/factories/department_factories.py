from tests.factories import *
from dartplan.models import Department


class DepartmentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Department

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: "Department %d" % n)
    abbr = factory.Sequence(lambda n: "D%d" % n)
