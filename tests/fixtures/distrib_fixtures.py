import pytest
from tests.factories import distributive_factories


@pytest.fixture()
def distrib(request):
    return distributive_factories.DistributiveFactory()
