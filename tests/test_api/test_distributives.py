import pytest
import json

from . import TestBase


class TestDistributiveListAPI(TestBase):
    def test_get_distributives(self, test_client, user, distrib):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': user.netid}

        r = test_client.get('/api/distributives')
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)

        assert len(data['distributives']) == 1
        assert data['distributives'][0]['abbr'] == distrib.abbr
