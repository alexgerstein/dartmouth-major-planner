import pytest
from tests.factories import term_factories


@pytest.fixture()
def term(request):
    return term_factories.TermFactory()


@pytest.fixture()
def oldTerm(request):
    return term_factories.TermFactory(year=1999)
