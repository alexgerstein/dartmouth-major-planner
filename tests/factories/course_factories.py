from tests.factories import *
from dartplan.models import Course
import factory.fuzzy

from department_factories import DepartmentFactory


class CourseFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Course

    id = factory.Sequence(lambda n: n)
    number = factory.fuzzy.FuzzyDecimal(99.0, precision=1)
    department = factory.SubFactory(DepartmentFactory)
    name = factory.Sequence(lambda n: "Course %d" % n)
    avg_median = factory.fuzzy.FuzzyChoice(['A', 'B', 'C', 'D'])
