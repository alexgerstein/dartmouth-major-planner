import pytest
from tests.factories import user_factories


@pytest.fixture()
def user(request):
    return user_factories.UserFactory(grad_year=2016)


@pytest.fixture()
def enrolled_user(request, offering):
    return user_factories.UserFactory(grad_year=offering.term.year + 1,
                                      offerings=[offering])


@pytest.fixture()
def enrolled_sole_user(request, user_added_offering):
    return user_factories.UserFactory(grad_year=user_added_offering.term.year + 1, offerings=[user_added_offering])
