import pytest
import json

from . import TestBase


class TestHourListAPI(TestBase):
    def test_get_hours(self, test_client, user, hour):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': user.netid}

        r = test_client.get('/api/hours')
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)

        assert len(data['hours']) == 1
        assert data['hours'][0]['period'] == hour.period
