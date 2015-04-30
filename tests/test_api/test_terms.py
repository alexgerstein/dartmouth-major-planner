import pytest
import json

from . import TestBase


class TestTermAPI(TestBase):

    def test_take_off_term(self, test_client, user):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': user.netid}

        term = user.terms.first()
        off = dict(on=False)
        take_off = test_client.put('/api/terms/%d' % term.id, data=off)
        self.check_valid_header_type(take_off.headers)

        data = json.loads(take_off.data)
        assert term not in user.terms
        assert data['term']['on'] == False

    def test_take_off_term_already_off(self, test_client, db, user, oldTerm):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': user.netid}

        off = dict(on=False)
        take_off = test_client.put('/api/terms/%d' % oldTerm.id, data=off)
        self.check_valid_header_type(take_off.headers)
        assert take_off.status_code == 409

        data = json.loads(take_off.data)
        assert oldTerm not in user.terms
        assert "Term is already marked off." in data['errors']['on'][0]
