import pytest
import json

from . import TestBase


class TestOfferingListAPI(TestBase):
    def test_create_offering(self, test_client, plan, course):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': plan.user.netid}

        term = plan.terms.first()
        data = {'course_id': course.id, 'term_id': term.id}
        r = test_client.post('/api/plans/%d/offerings' % plan.id, data=data)
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        assert data['offering']['term']['id'] == term.id
        assert plan.offerings.count() == 1


class TestOfferingAPI(TestBase):
    def test_put_enroll(self, test_client, offering, plan):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': plan.user.netid}

        data = {'enrolled': True}

        r = test_client.put('/api/plans/%d/offerings/%d' % (plan.id,
                                                            offering.id),
                            data=data)
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        assert data['offering']['enrolled'] is True
        assert plan.offerings.count() == 1

    def test_put_unenroll(self, test_client, plan_with_offering):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': plan_with_offering.user.netid}

        offering = plan_with_offering.offerings.first()
        data = {'enrolled': False}
        r = test_client.put('/api/plans/%d/offerings/%d' %
                            (plan_with_offering.id, offering.id), data=data)
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        assert not data['offering']['enrolled']
        assert plan_with_offering.offerings.count() == 0

    def test_put_unenroll_sole_user_added(self, test_client,
                                          plan_with_user_added_offering):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': plan_with_user_added_offering.user.netid}

        offering = plan_with_user_added_offering.offerings.first()
        data = {'enrolled': False}
        r = test_client.put('/api/plans/%d/offerings/%d' %
                            (plan_with_user_added_offering.id, offering.id),
                            data=data)
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        assert data['offering'] is None

        r = test_client.get('/api/offerings/%d' % offering.id)
        assert r.headers['Content-Type'] != 'application/json'


class TestCourseOfferingListAPI(TestBase):
    def test_get_offerings(self, test_client, plan_with_offering):
        offering = plan_with_offering.offerings.first()
        r = test_client.get('/api/plans/%d/courses/%d/offerings' % (plan_with_offering.id, offering.course.id))
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        assert data['offerings'][0]['name'] == str(offering)
