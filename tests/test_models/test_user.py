import pytest
from dartplan.models import User


class TestUser():

    def test_user_get_id(self, user):
        assert user.get_id() == unicode(user.id)
