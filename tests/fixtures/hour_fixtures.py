import pytest
from tests.factories import hour_factories


@pytest.fixture()
def hour(db):
    hour = hour_factories.HourFactory()
    db.session.commit()
    return hour
