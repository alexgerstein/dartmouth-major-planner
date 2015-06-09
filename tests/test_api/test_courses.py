import pytest
import json

from . import TestBase

MEDIANS = ['A', 'A/A-', 'A-', 'A-/B+', 'B+', 'B+/B', 'B', 'B/B-',
           'B-', 'B-/C+', 'C+', 'C+/C', 'C']


class TestCourseAPI(TestBase):
    def test_get_course(self, test_client, course):
        get = test_client.get('/api/courses/%d' % course.id)
        self.check_valid_header_type(get.headers)
        data = json.loads(get.data)
        assert data['course']['name'] == course.name


class TestCourseListAPI(TestBase):
    def test_get_courses(self, test_client, course_with_user_added_offering):
        get = test_client.get('/api/courses')
        self.check_valid_header_type(get.headers)
        data = json.loads(get.data)
        assert len(data['courses']) == 1

    def test_get_courses_by_dept(self, test_client,
                                 course_with_user_added_offering):
        query_data = {'dept_id': course_with_user_added_offering.department.id}
        get = test_client.get('/api/courses', query_string=query_data)
        self.check_valid_header_type(get.headers)
        data = json.loads(get.data)
        assert len(data['courses']) == 1

    def test_get_courses_by_term(self, test_client,
                                 course_with_user_added_offering):
        offering = course_with_user_added_offering.offerings[0]

        query_data = {'term_id': offering.term.id}
        get = test_client.get('/api/courses', query_string=query_data)
        self.check_valid_header_type(get.headers)
        data = json.loads(get.data)
        assert len(data['courses']) == 1

    def test_get_courses_by_hour(self, test_client,
                                 course_with_user_added_offering):
        offering = course_with_user_added_offering.offerings[0]

        query_data = {'hour_id': offering.hour.id}
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
        median_id = MEDIANS.index(course_with_user_added_offering.avg_median)
        query_data = {'median_id': median_id}
        get = test_client.get('/api/courses', query_string=query_data)
        self.check_valid_header_type(get.headers)
        data = json.loads(get.data)
        assert len(data['courses']) == 1
