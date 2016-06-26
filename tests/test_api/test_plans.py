import pytest
import json

from . import TestBase


class TestPlanListAPI(TestBase):
    def test_get_plans(self, test_client, user_with_two_plans):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': user_with_two_plans.netid}

        r = test_client.get('/api/plans')
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        plans_data = data['plans']
        assert len(plans_data) == 2

        first_plan = plans_data[0]
        second_plan = plans_data[1]
        assert first_plan.get('id')
        assert second_plan.get('id')
        assert first_plan.get('id') != second_plan.get('id')

    def test_post_plans(self, test_client, pro_user):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': pro_user.netid}

        data = {'title': 'My Plan', 'fifth_year': True}

        r = test_client.post('/api/plans', data=data)
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        plan_data = data['plan']
        assert plan_data.get('id')
        assert plan_data.get('title') == 'My Plan'
        assert plan_data.get('fifth_year')

    def test_post_plans_unauthorized(self, test_client, plan):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': plan.user.netid}

        data = {'title': 'My Plan', 'fifth_year': True}

        r = test_client.post('/api/plans', data=data)
        self.check_valid_header_type(r.headers)
        assert r.status_code == 401


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
        assert not plan_data['default']
        assert plan_data['offerings'][0]['name'] == str(offering)

    def test_change_plan_title(self, test_client, plan):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': plan.user.netid}

        title = dict(title='New Title')
        r = test_client.put('/api/plans/%d' % plan.id, data=title)
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        plan_data = data['plan']
        assert plan_data['title'] == 'New Title'

    def test_set_default(self, test_client, plan_with_offering):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': plan_with_offering.user.netid}

        default_plan = dict(default=True)
        set_default_plan = test_client.put('/api/plans/%d' %
                                           (plan_with_offering.id),
                                           data=default_plan)
        self.check_valid_header_type(set_default_plan.headers)

        data = json.loads(set_default_plan.data)

        assert data['plan']['default'] is True

    def test_enroll_in_fifth_year(self, test_client, plan_with_offering):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': plan_with_offering.user.netid}

        fifth_year = dict(fifth_year=True)
        enroll_in_extra_year = test_client.put('/api/plans/%d' %
                                               (plan_with_offering.id),
                                               data=fifth_year)
        self.check_valid_header_type(enroll_in_extra_year.headers)

        data = json.loads(enroll_in_extra_year.data)

        assert data['plan']['fifth_year'] is True

    def test_enroll_in_fifth_year_already_enrolled(self, test_client,
                                                   five_year_plan):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': five_year_plan.user.netid}

        fifth_year = dict(fifth_year=True)
        enroll_in_extra_year = test_client.put('/api/plans/%d' %
                                               (five_year_plan.id),
                                               data=fifth_year)
        self.check_valid_header_type(enroll_in_extra_year.headers)
        assert enroll_in_extra_year.status_code == 409

        data = json.loads(enroll_in_extra_year.data)
        assert "Plan already has 5th year" in data['errors']['fifth_year'][0]

    def test_unenroll_in_fifth_year_already_unenrolled(self, test_client,
                                                       plan):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': plan.user.netid}

        fifth_year = dict(fifth_year=False)
        enroll_in_extra_year = test_client.put('/api/plans/%d' %
                                               (plan.id), data=fifth_year)
        self.check_valid_header_type(enroll_in_extra_year.headers)
        assert enroll_in_extra_year.status_code == 409

        data = json.loads(enroll_in_extra_year.data)
        assert "Plan already excludes 5th year" in data['errors']['fifth_year'][0]

    def test_enroll_in_fifth_year_unauthorized(self, test_client, user,
                                               plan_with_offering):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': user.netid}

        fifth_year = dict(fifth_year=True)
        enroll_in_extra_year = test_client.put('/api/plans/%d' %
                                               (plan_with_offering.id),
                                               data=fifth_year)
        self.check_valid_header_type(enroll_in_extra_year.headers)
        assert enroll_in_extra_year.status_code == 401
