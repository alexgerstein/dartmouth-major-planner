import pytest
from tests.factories import term_factories


@pytest.fixture()
def term(db):
    term = term_factories.TermFactory()
    db.session.commit()
    return term


@pytest.fixture()
def oldTerm(db):
    term = term_factories.TermFactory(year=1999)
    db.session.commit()
    return term
