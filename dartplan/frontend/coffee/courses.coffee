dartplanApp = angular.module 'dartplanApp'

dartplanApp.factory 'Course', ->
  class Course
    constructor: (options) ->
      {@id, @full_name} = options

dartplanApp.factory 'CourseService', ['$http', 'Course', ($http, Course) ->
  new class Search
    search: (options) ->
      $http.get('/api/courses', {params: options}).then (result) ->
        new Course course for course in result.data.courses
]
