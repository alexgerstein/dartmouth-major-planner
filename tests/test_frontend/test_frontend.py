import pytest
from dartplan.models import User


class TestHomePage:

    def test_home_page(self, test_client):
        rv = test_client.get('/')
        assert "DARTPlan" in rv.data

    def test_index_page(self, test_client):
        rv = test_client.get('/index')
        assert "DARTPlan" in rv.data

    def test_api_request_new_user(self, test_client, offering):
        with test_client.session_transaction() as sess:
            sess['user'] = {'netid': 'd36395d', 'name': 'Alex Gerstein'}

        data = dict(enrolled=True)
        rv = test_client.put('/api/offerings/%d' % offering.id, data)
        rv.status_code == 303
        assert User.query.filter_by(netid='d36395d').first()
