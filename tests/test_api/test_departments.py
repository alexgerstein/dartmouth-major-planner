import pytest
import json

from . import TestBase


class TestDepartmentListAPI(TestBase):
    def test_get_departments(self, test_client, user, department):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': user.netid}

        r = test_client.get('/api/departments')
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)

        assert len(data['departments']) == 1
        assert data['departments'][0]['abbr'] == department.abbr
