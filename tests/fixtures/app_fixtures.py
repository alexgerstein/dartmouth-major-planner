import pytest

from dartplan import create_app
from dartplan.database import db as _db
from dartplan.mail import mail


@pytest.yield_fixture
def app(request):
    """Session-wide test `Flask` application"""
    _app = create_app("testing")

    # Establish an application context before running the tests.
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(autouse=True)
def db(app, request):
    """Session-wide test database"""

    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.yield_fixture
def test_client(app, request):
    with app.test_client() as client:
        yield client


@pytest.yield_fixture
def outbox(request):
    with mail.record_messages() as outbox:
        yield outbox
