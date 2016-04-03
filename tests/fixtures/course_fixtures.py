import pytest
from tests.factories import course_factories


@pytest.fixture()
def course(db):
    course = course_factories.CourseFactory()
    db.session.commit()
    return course


@pytest.fixture()
def course_with_registrar_added_offering(db, registrar_added_offering):
    course = course_factories.CourseFactory(offerings=[registrar_added_offering])
    db.session.commit()
    return course


@pytest.fixture()
def course_with_user_added_offering(db, user_added_offering):
    course = course_factories.CourseFactory(offerings=[user_added_offering])
    db.session.commit()
    return course
