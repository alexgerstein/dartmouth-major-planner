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


class TestCourseListAPI(TestBase):
    def test_get_courses(self, test_client, course_with_user_added_offering):
        get = test_client.get('/api/courses')
        self.check_valid_header_type(get.headers)
        data = json.loads(get.data)
        assert len(data['courses']) == 1

    def test_get_courses_by_dept(self, test_client,
                                 course_with_user_added_offering):
        query_data = {'department_id': course_with_user_added_offering.department_id}
        get = test_client.get('/api/courses', query_string=query_data)
        self.check_valid_header_type(get.headers)
        data = json.loads(get.data)
        assert len(data['courses']) == 1

    def test_get_courses_by_term(self, test_client,
                                 course_with_user_added_offering):
        offering = course_with_user_added_offering.offerings[0]

        query_data = {'term_id': offering.term_id}
        get = test_client.get('/api/courses', query_string=query_data)
        self.check_valid_header_type(get.headers)
        data = json.loads(get.data)
        assert len(data['courses']) == 1

    def test_get_courses_by_hour(self, test_client,
                                 course_with_user_added_offering):
        offering = course_with_user_added_offering.offerings[0]

        query_data = {'hour_id': offering.hour_id}
        get = test_client.get('/api/courses', query_string=query_data)
        self.check_valid_header_type(get.headers)
        data = json.loads(get.data)
        assert len(data['courses']) == 1

    def test_get_courses_by_distrib(self, test_client,
                                    course_with_user_added_offering):
        offering = course_with_user_added_offering.offerings[0]

        query_data = {'distrib_id': offering.distributives.first().id}
        get = test_client.get('/api/courses', query_string=query_data)
        self.check_valid_header_type(get.headers)
        data = json.loads(get.data)
        assert len(data['courses']) == 1

    def test_get_courses_by_median(self, test_client,
                                   course_with_user_added_offering):
        query_data = {'median_id': 12}
        get = test_client.get('/api/courses', query_string=query_data)
        self.check_valid_header_type(get.headers)
        data = json.loads(get.data)
        assert len(data['courses']) == 1
