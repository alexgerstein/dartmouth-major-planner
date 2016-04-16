import pytest
from tests.factories import offering_factories


@pytest.fixture()
def offering(db, distrib):
    offering = offering_factories.OfferingFactory(distributives=[distrib])
    db.session.commit()
    return offering


@pytest.fixture()
def user_added_offering(db, distrib):
    offering = offering_factories.OfferingFactory(user_added="Y",
                                                  distributives=[distrib])
    db.session.commit()
    return offering


@pytest.fixture()
def registrar_added_offering(db, distrib):
    offering = offering_factories.OfferingFactory(user_added="N",
                                                  distributives=[distrib])
    db.session.commit()
    return offering
