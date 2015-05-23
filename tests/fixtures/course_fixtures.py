import pytest
from tests.factories import course_factories


@pytest.fixture()
def course(request):
    return course_factories.CourseFactory()


@pytest.fixture()
def course_with_registrar_added_offering(request, registrar_added_offering):
    return course_factories.CourseFactory(offerings=[registrar_added_offering])


@pytest.fixture()
def course_with_user_added_offering(request, user_added_offering):
    return course_factories.CourseFactory(offerings=[user_added_offering])
