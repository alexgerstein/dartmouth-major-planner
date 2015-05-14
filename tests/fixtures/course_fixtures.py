import pytest
from tests.factories import (course_factories, offering_factories,
                             distributive_factories)


@pytest.fixture()
def course(request):
    return course_factories.CourseFactory()


@pytest.fixture()
def course_with_registrar_added_offering(request):
    course = course_factories.CourseFactory()
    distrib = distributive_factories.DistributiveFactory()
    offering = offering_factories.OfferingFactory(user_added="N",
                                                  course_id=course.id,
                                                  distributives=[distrib])
    course.offerings.append(offering)
    return course


@pytest.fixture()
def course_with_user_added_offering(request):
    course = course_factories.CourseFactory()
    distrib = distributive_factories.DistributiveFactory()
    offering = offering_factories.OfferingFactory(user_added="Y",
                                                  course_id=course.id,
                                                  distributives=[distrib])
    course.offerings.append(offering)
    return course
