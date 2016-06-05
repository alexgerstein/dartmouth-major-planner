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
    getCourseOfferings: (id) ->
      $http.get("/api/courses/#{ id }/offerings").then (result) =>
        new Offering offering for offering in result.data.offerings

    toggle: (plan_id, id, enrolled) ->
      $http.put("/api/plans/#{plan_id}/offerings/#{id}", {'enrolled': enrolled}).then (result) ->
        $rootScope.$broadcast 'changedCourses'
        $mdToast.showSimple('Successfully changed course enrollment.');

        if enrolled
          ll('tagEvent', 'Course enrolled', {'offering_id': id, 'plan_id': plan_id})
        else
          ll('tagEvent', 'Course unenrolled', {'offering_id': id, 'plan_id': plan_id})

    enrollCustomOffering: (plan_id, course_id, term_id) ->
      $http.post("/api/plans/#{plan_id}/offerings", {course_id: course_id, term_id: term_id}).then (result) ->
        $rootScope.$broadcast 'changedCourses'
        $mdToast.showSimple('Successfully changed course enrollment.');
        new Offering result.data.offering
        ll('tagEvent', 'Course enrolled', {'course_id': course_id, 'term_id': term_id, 'plan_id': plan_id})
]
