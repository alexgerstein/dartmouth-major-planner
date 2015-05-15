import pytest
import json

from . import TestBase


class TestOfferingListAPI(TestBase):
    def test_create_offering(self, test_client, user, course):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': user.netid}

        term = user.terms.first()
        data = {'course_id': course.id, 'term_id': term.id}
        r = test_client.post('/api/offerings', data=data)
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)



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
        assert data['offering']['enrolled']

    def test_put_unenroll(self, test_client, enrolled_user):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': enrolled_user.netid}

        offering = enrolled_user.courses.first()
        data = {'enrolled': False}
        r = test_client.put('/api/offerings/%d' % offering.id, data=data)
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)
        assert not data['offering']['enrolled']
