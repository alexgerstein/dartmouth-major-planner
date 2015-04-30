class TestBase:

    def check_valid_header_type(self, headers):
        assert headers['Content-Type'] == 'application/json'
