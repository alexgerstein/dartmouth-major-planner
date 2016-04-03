import pytest
from tests.factories import distributive_factories


@pytest.fixture()
def distrib(db):
    distrib = distributive_factories.DistributiveFactory()
    db.session.commit()
    return distrib
