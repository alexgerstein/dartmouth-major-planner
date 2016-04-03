import pytest
import json

from . import TestBase


class TestOfferingListAPI(TestBase):
    def test_get_users_offerings(self, test_client, enrolled_user):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': enrolled_user.netid}

        r = test_client.get('/api/offerings')
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        assert data['offerings'][0]['name'] == str(enrolled_user.courses.first())

    def test_create_offering(self, test_client, user, course):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': user.netid}

        term = user.terms.first()
        plan = user.plans.first()
        data = {'course_id': course.id, 'term_id': term.id}
        r = test_client.post('/api/offerings', data=data)
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        assert data['offering']['term']['id'] == term.id
        assert user.courses.count() == 1
        assert plan.offerings.count() == 1


class TestOfferingAPI(TestBase):
    def test_get_offering(self, test_client, offering):
        r = test_client.get('/api/offerings/%d' % offering.id)
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        assert data['offering']['name'] == str(offering)

    def test_get_offering_signed_in(self, test_client, offering, user):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': user.netid}

        r = test_client.get('/api/offerings/%d' % offering.id)
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        assert not data['offering']['enrolled']

    def test_put_enroll(self, test_client, offering, user):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': user.netid}

        data = {'enrolled': True}

        r = test_client.put('/api/offerings/%d' % offering.id, data=data)
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        assert data['offering']['enrolled'] is True
        assert user.courses.count() == 1
        assert user.plans.first().offerings.count() == 1

    def test_put_unenroll(self, test_client, enrolled_user):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': enrolled_user.netid}

        offering = enrolled_user.courses.first()
        data = {'enrolled': False}
        r = test_client.put('/api/offerings/%d' % offering.id, data=data)
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        assert not data['offering']['enrolled']
        assert enrolled_user.courses.count() == 0
        assert enrolled_user.plans.first().offerings.count() == 0

    def test_put_unenroll_sole_user_added(self, test_client,
                                          enrolled_sole_user):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': enrolled_sole_user.netid}

        offering = enrolled_sole_user.courses.first()
        data = {'enrolled': False}
        r = test_client.put('/api/offerings/%d' % offering.id, data=data)
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        assert data['offering'] is None

        r = test_client.get('/api/offerings/%d' % offering.id)
        assert r.status_code == 404


class TestCourseOfferingListAPI(TestBase):
    def test_get_offerings(self, test_client, offering):
        r = test_client.get('/api/courses/%d/offerings' % offering.course.id)
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        assert data['offerings'][0]['name'] == str(offering)
