import pytest
import json

from . import TestBase


class TestCourseAPI(TestBase):
    def test_get_course(self, test_client, course):
        get = test_client.get('/api/courses/%d' % course.id)
        self.check_valid_header_type(get.headers)

    def test_get_course_with_official_offering(self, test_client,
                                               course_with_registrar_added_offering):
        offering = course_with_registrar_added_offering.offerings[0]
        get = test_client.get('/api/courses/%d' %
                              course_with_registrar_added_offering.id)
        self.check_valid_header_type(get.headers)
        data = json.loads(get.data)
        assert data['course']['terms'][0]['term'] == str(offering.term)

    def test_get_course_with_user_offering(self, test_client,
                                           course_with_user_added_offering):
        offering = course_with_user_added_offering.offerings[0]
        get = test_client.get('/api/courses/%d' %
                              course_with_user_added_offering.id)
        self.check_valid_header_type(get.headers)
        data = json.loads(get.data)
        assert data['course']['user_terms'][0]['term'] == str(offering.term)
