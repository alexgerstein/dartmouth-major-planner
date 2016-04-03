import pytest
import json

from . import TestBase


class TestPlanAPI(TestBase):

    def test_get_plan(self, test_client, plan_with_offering):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': plan_with_offering.user.netid}

        r = test_client.get('/api/plans/%d' % plan_with_offering.id)
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        plan_data = data['plan']
        offering = plan_with_offering.offerings.first()
        assert plan_data['title'] == 'Default'
        assert plan_data['offerings'][0]['name'] == str(offering)
