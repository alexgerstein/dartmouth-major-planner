import pytest
import json

from . import TestBase


class TestMedianListAPI(TestBase):
    def test_get_hours(self, test_client, user):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': user.netid}

        r = test_client.get('/api/medians')
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)

        assert len(data['medians']) == 13
        assert data['medians'][0]['id'] == 0
        assert data['medians'][0]['value'] == 'A'
