import pytest
from tests.factories import user_factories


@pytest.fixture()
def user(db):
    user = user_factories.UserFactory()
    db.session.commit()
    return user
