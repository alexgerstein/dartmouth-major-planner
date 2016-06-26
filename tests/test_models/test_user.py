import pytest
from dartplan.models import User


class TestUser():

    def test_user_get_id(self, user):
        assert user.get_id() == unicode(user.id)

    def test_user_is_pro(self, user):
        assert not user.is_pro()

        user.amount_paid = 10
        assert user.is_pro()

        user.amount_paid = 0
        assert not user.is_pro()
