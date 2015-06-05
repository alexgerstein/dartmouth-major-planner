dartplanApp = angular.module 'dartplanApp'

dartplanApp.factory 'Offering', ['Term', 'Course', (Term, Course) ->
  class Offering
    constructor: (options) ->
      {@id, @name, @hour, @info, @enrolled, @enrollment, @user_added} = options
      @term = new Term options.term
      @course = new Course options.course
]

dartplanApp.factory 'OfferingsService', ['$http', '$rootScope', '$mdToast', 'Offering', ($http, $rootScope, $mdToast, Offering) ->
  new class Offerings
    getEnrolled: ->
      $http.get('/api/offerings').then (result) ->
        new Offering offering for offering in result.data.offerings

    getCourseOfferings: (id) ->
      $http.get("/api/courses/#{ id }/offerings").then (result) =>
        new Offering offering for offering in result.data.offerings

    toggle: (id, enrolled) ->
      $http.put("/api/offerings/#{ id }", {'enrolled': enrolled}).then (result) ->
        $rootScope.$broadcast 'changedCourses'
        $mdToast.showSimple('Successfully changed course enrollment.');

    enrollCustomOffering: (course_id, term_id) ->
      $http.post("/api/offerings", {course_id: course_id, term_id: term_id}).then (result) ->
        $rootScope.$broadcast 'changedCourses'
        $mdToast.showSimple('Successfully changed course enrollment.');
]
