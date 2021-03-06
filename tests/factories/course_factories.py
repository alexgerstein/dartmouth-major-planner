from tests.factories import *
from dartplan.models import Course
import factory.fuzzy

from department_factories import DepartmentFactory


class CourseFactory(BaseFactory):
    class Meta:
        model = Course

    number = factory.fuzzy.FuzzyDecimal(99.0, precision=1)
    department = factory.SubFactory(DepartmentFactory)
    name = factory.Sequence(lambda n: "Course %d" % n)
    avg_median = factory.fuzzy.FuzzyChoice(['A', 'B', 'C'])

    @factory.post_generation
    def offerings(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for offering in extracted:
                self.offerings.append(offering)
