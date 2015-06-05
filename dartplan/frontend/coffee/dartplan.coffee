dartplanApp = angular.module 'dartplanApp', ['ngMaterial', 'ngMdIcons']

class config
  constructor: ($interpolateProvider, $mdThemingProvider) ->
    $interpolateProvider
      .startSymbol '{['
      .endSymbol ']}'

    $mdThemingProvider.theme 'default'
      .primaryPalette 'green'
      .accentPalette 'orange'

dartplanApp.config config

dartplanApp.factory 'TermsService', ['$http', '$rootScope', '$mdToast', 'Term', ($http, $rootScope, $mdToast, Term) ->
  new class Terms
    getUserTerms: ->
      $http.get('/api/terms').then (result) ->
        new Term term for term in result.data.terms

    toggle: (id, enrolled) ->
      $http.put("/api/terms/#{ id }", {'on': enrolled}).then (result) ->
        $rootScope.$broadcast 'changedCourses'
        $mdToast.showSimple('Successfully changed term enrollment.');
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

dartplanApp.factory 'CourseService', ['$http', 'Course', ($http, Course) ->
  new class Search
    search: (options) ->
      $http.get('/api/courses', {params: options}).then (result) ->
        new Course course for course in result.data.courses
]

dartplanApp.factory 'Term', ->
  class Term
    constructor: (options) ->
      {@id, @abbr, @on} = options

dartplanApp.factory 'Course', ->
  class Course
    constructor: (options) ->
      {@id, @full_name} = options

dartplanApp.factory 'Offering', ['Term', 'Course', (Term, Course) ->
  class Offering
    constructor: (options) ->
      {@id, @name, @hour, @info, @enrolled, @enrollment, @user_added} = options
      @term = new Term options.term
      @course = new Course options.course
]

dartplanApp.controller 'PlannerController', ['$scope', '$mdDialog', '$sce', 'TermsService', 'OfferingsService', ($scope, $mdDialog, $sce, TermsService, OfferingsService) ->

  render = ->
    $scope.term = []
    $scope.offerings = []

    TermsService.getUserTerms().then (terms) ->
      $scope.terms = terms

    OfferingsService.getEnrolled().then (offerings) ->
      $scope.offerings = offerings

  render()

  $scope.toggleTerm = (term) =>
    TermsService.toggle(term.id, !term.on)

  $scope.$on 'changedCourses', =>
    render()

  $scope.showOfferingInfoModal = (offering) ->
    $scope.offering = offering
    $scope.info_html = $sce.trustAsHtml(offering.info)
    $mdDialog.show({
          controller: OfferingInfoDialogController,
          scope: $scope,
          preserveScope: true,
          templateUrl: 'static/partials/offering-info-dialog.html',
          clickOutsideToClose: true
        })
]

OfferingInfoDialogController = ($scope, $mdDialog) ->
  $scope.cancel = ->
    $mdDialog.cancel()

CourseDialogController = ($scope, $mdDialog, OfferingsService) ->
  $scope.toggleEnroll = (offering) ->
    OfferingsService.toggle(offering.id, !offering.enrolled)
    $mdDialog.hide()

  $scope.enrollCustomOffering = ->
    OfferingsService.enrollCustomOffering($scope.course.id, $scope.custom.term_id)
    $mdDialog.hide()

  $scope.cancel = ->
    $mdDialog.cancel()

CourseDialogLauncherController = ($scope, $mdDialog, OfferingsService, TermsService) ->
  $scope.custom = {}

  $scope.showTermModal = (course) ->
    $scope.course = course
    $scope.offeringsLoading = true
    $scope.customTermsLoading = true
    OfferingsService.getCourseOfferings(course.id).then (offerings) ->
      $scope.offerings = offerings
      $scope.offeringsLoading = false

    TermsService.getUserTerms().then (terms) ->
      $scope.customUserTerms = terms
      $scope.customTermsLoading = false

    $mdDialog.show({
      controller: CourseDialogController,
      scope: $scope,
      preserveScope: true,
      templateUrl: 'static/partials/course-dialog.html',
      clickOutsideToClose: true
    })

dartplanApp.controller 'SearchController', ['$rootScope', '$scope', '$mdDialog', 'CourseService', ($rootScope, $scope, $mdDialog, CourseService) ->
  $scope.fields = {}

  $scope.submit = ->
    $scope.loading = true
    CourseService.search($scope.fields).then (courses) ->
      $scope.courses = courses
      $scope.loading = false
]

dartplanApp.directive 'courseSearchResult', ->
  return {
    replace: true,
    templateUrl: 'static/partials/course-search-result.html',
    controller: CourseDialogLauncherController
  }

dartplanApp.directive 'termOffering', ->
  return {
    replace: true,
    templateUrl: 'static/partials/term-offering.html',
    controller: CourseDialogLauncherController
  }
