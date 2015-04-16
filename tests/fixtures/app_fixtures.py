import pytest

from sqlalchemy.orm import Session, scoped_session, sessionmaker
from dartplan import create_app
from dartplan.database import db as _db


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

    options = dict()
    session = db.create_scoped_session(options)
    db.session = session

    yield db.session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.yield_fixture()
def test_client(app, request):
    with app.test_client() as client:
        yield client
