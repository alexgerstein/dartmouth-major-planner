import pytest
from tests.factories import offering_factories


@pytest.fixture()
def offering(request):
    return offering_factories.OfferingFactory()
