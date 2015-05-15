import pytest
from tests.factories import user_factories


@pytest.fixture()
def user(request):
    return user_factories.UserFactory(grad_year=2016)


@pytest.fixture()
def enrolled_user(request, offering):
    return user_factories.UserFactory(offerings=[offering])
