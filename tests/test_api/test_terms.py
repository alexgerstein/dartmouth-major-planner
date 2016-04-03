import pytest
import json

from . import TestBase


class TestTermListAPI(TestBase):
    def test_get_user_enrolled_terms(self, test_client, plan):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': plan.user.netid}

        r = test_client.get('/api/terms')
        self.check_valid_header_type(r.headers)
        data = json.loads(r.data)

        assert len(data['terms']) == 16


class TestTermAPI(TestBase):

    def test_take_off_term(self, test_client, plan_with_offering):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': plan_with_offering.user.netid}

        offering = plan_with_offering.offerings.first()
        term = offering.term
        off = dict(on=False)
        take_off = test_client.put('/api/terms/%d' % term.id, data=off)
        self.check_valid_header_type(take_off.headers)

        data = json.loads(take_off.data)
        assert term not in plan_with_offering.terms
        assert offering not in plan_with_offering.offerings
        assert data['term']['on'] is False

    def test_take_off_term_already_off(self, test_client, plan, oldTerm):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': plan.user.netid}

        off = dict(on=False)

        take_off = test_client.put('/api/terms/%d' % oldTerm.id, data=off)
        self.check_valid_header_type(take_off.headers)
        assert take_off.status_code == 409

        data = json.loads(take_off.data)
        assert oldTerm not in plan.terms
        assert "Term is already marked off." in data['errors']['on'][0]

    def test_enroll_term(self, test_client, plan, oldTerm):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': plan.user.netid}

        on = dict(on=True)
        enroll = test_client.put('/api/terms/%d' % oldTerm.id, data=on)
        self.check_valid_header_type(enroll.headers)

        data = json.loads(enroll.data)
        assert oldTerm in plan.terms
        assert data['term']['on'] is True

    def test_enroll_term_already_on(self, test_client, plan):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': plan.user.netid}

        term = plan.terms.first()
        on = dict(on=True)

        enroll = test_client.put('/api/terms/%d' % term.id, data=on)
        self.check_valid_header_type(enroll.headers)
        assert enroll.status_code == 409

        data = json.loads(enroll.data)
        assert term in plan.terms
        assert "Term is already marked on." in data['errors']['on'][0]
