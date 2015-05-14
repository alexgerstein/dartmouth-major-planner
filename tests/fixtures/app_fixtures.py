import pytest

from dartplan import create_app
from dartplan.database import db as _db
from tests.factories import (user_factories, term_factories, course_factories,
                             department_factories, offering_factories,
                             hour_factories)


@pytest.yield_fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application"""
    app = create_app("testing")

    # Establish an application context before running the tests.
    ctx = app.test_request_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.yield_fixture(scope='session')
def db(app, request):
    """Session-wide test database"""

    _db.drop_all()
    _db.create_all()
    _db.app = app

    yield _db


@pytest.yield_fixture(autouse=True)
def session(db, request):
    """Creates a new database session for a test."""
    # connect to the database
    connection = db.engine.connect()

    # begin a non-ORM transaction
    transaction = connection.begin()

    options = dict(bind=connection)
    session = db.create_scoped_session(options)
    db.session = session

    user_factories.UserFactory._meta.sqlalchemy_session = session
    term_factories.TermFactory._meta.sqlalchemy_session = session
    course_factories.CourseFactory._meta.sqlalchemy_session = session
    department_factories.DepartmentFactory._meta.sqlalchemy_session = session
    offering_factories.OfferingFactory._meta.sqlalchemy_session = session
    hour_factories.HourFactory._meta.sqlalchemy_session = session

    yield db.session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.yield_fixture()
def test_client(app, request):
    with app.test_client() as client:
        yield client
