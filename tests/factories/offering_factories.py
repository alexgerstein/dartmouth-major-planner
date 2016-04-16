from tests.factories import *
from dartplan.models import Offering
from term_factories import TermFactory
from hour_factories import HourFactory
from course_factories import CourseFactory
import factory.fuzzy


class OfferingFactory(BaseFactory):
    class Meta:
        model = Offering

    term = factory.SubFactory(TermFactory)
    hour = factory.SubFactory(HourFactory)
    course = factory.SubFactory(CourseFactory)
    desc = factory.Sequence(lambda n: "Course %d covers stuff..." % n)

    median = factory.fuzzy.FuzzyChoice(['A', 'B', 'C', 'D'])

    added = factory.Iterator(['F'])
    user_added = "N"

    @factory.post_generation
    def distributives(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for distrib in extracted:
                self.distributives.append(distrib)
