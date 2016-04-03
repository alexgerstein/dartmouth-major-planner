import pytest
import json

from . import TestBase


class TestPlanAPI(TestBase):

    def test_get_plan(self, test_client, user):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': user.netid}

        plan = user.plans.first()
        r = test_client.get('/api/plans/%d' % plan.id)
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        assert data['plan']['title'] == plan.title
