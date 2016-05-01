import pytest


class TestAdmin:

    def test_home_page_not_authenticated(self, test_client):
        rv = test_client.get('/admin/userview/')
        assert rv.status_code == 302
