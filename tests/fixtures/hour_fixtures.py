import pytest
from tests.factories import hour_factories


@pytest.fixture()
def hour(request):
    return hour_factories.HourFactory()
