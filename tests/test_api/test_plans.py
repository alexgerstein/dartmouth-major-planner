import pytest
import json

from . import TestBase


class TestPlanAPI(TestBase):

    def test_get_plan(self, test_client, enrolled_user):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': enrolled_user.netid}

        plan = enrolled_user.plans.first()
        r = test_client.get('/api/plans/%d' % plan.id)
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        plan_data = data['plan']
        assert plan_data['title'] == plan.title
        assert plan_data['offerings'][0]['name'] == str(plan.offerings.first())
