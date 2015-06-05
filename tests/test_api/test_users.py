import pytest
import json

from . import TestBase


class TestUserAPI(TestBase):

    def test_get_user(self, test_client, user):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': user.netid}

        r = test_client.get('/api/user')
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        assert data['user']['nickname'] == user.nickname

    def test_delete_user(self, test_client, user):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': user.netid}

        # Remove dummy user
        delete = test_client.delete('/api/user')
        self.check_valid_header_type(delete.headers)
        data = json.loads(delete.data)
        assert data['result'] == True

        # Dummy user should no longer be logged in
        get = test_client.delete('/api/user')
        assert "login" in get.data
        assert get.status_code == 302
