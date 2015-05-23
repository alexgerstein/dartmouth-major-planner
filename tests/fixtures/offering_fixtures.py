import pytest
from tests.factories import offering_factories


@pytest.fixture()
def offering(request, distrib):
    return offering_factories.OfferingFactory(distributives=[distrib])


@pytest.fixture()
def user_added_offering(request, distrib):
    return offering_factories.OfferingFactory(user_added="Y",
                                              distributives=[distrib])


@pytest.fixture()
def registrar_added_offering(request, distrib):
    return offering_factories.OfferingFactory(user_added="N",
                                              distributives=[distrib])
