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

dartplanApp.factory 'PlanService', ['$http', 'Offering', 'Term', ($http, Offering, Term) ->
  new class Plan
    all: ->
      $http.get('/api/plan').then (result) ->
        data = {'offerings': [], 'terms': []}
        data.offerings.push new Offering offering for offering in result.data.offerings
        data.terms.push new Term term for term in result.data.terms
        data
]

dartplanApp.factory 'SearchService', ['$http', 'Course', 'Offering', ($http, Course, Offering) ->
  new class Search
    search: (options) ->
      $http.get('/api/courses', {params: options}).then (result) ->
        new Course course for course in result.data.courses

    get_course_offerings: (course_id) ->
      $http.get("/api/courses/#{ course_id }/offerings").then (result) =>
        new Offering offering for offering in result.data.offerings
]

dartplanApp.factory 'Term', ['$http', '$rootScope', '$mdToast', ($http, $rootScope, $mdToast) ->
  class Term
    constructor: (options) ->
      {@id, @abbr, @on} = options

    toggle: ->
      $http.put("/api/terms/#{ @id }", {on: !@on}).then (result) ->
        $rootScope.$broadcast 'changedCourses'
        $mdToast.showSimple('Successfully changed term enrollment.');
]

dartplanApp.factory 'Offering', ['$http', '$rootScope', '$mdToast', 'Term', 'Course', ($http, $rootScope, $mdToast, Term, Course) ->
  class Offering
    constructor: (options) ->
      {@id, @name, @hour, @info, @enrolled, @enrollment} = options
      @term = new Term options.term
      @course = new Course options.course

    toggleEnroll: ->
      $http.put("/api/offerings/#{ @id }", {enrolled: !@enrolled}).then (result) ->
        $rootScope.$broadcast 'changedCourses'
        $mdToast.showSimple('Successfully changed course enrollment.');
]

dartplanApp.factory 'Course', ['$http', ($http) ->
  class Course
    constructor: (options) ->
      {@id, @full_name} = options
]

dartplanApp.controller 'PlannerController', ['$scope', '$mdDialog', '$sce', 'PlanService', ($scope, $mdDialog, $sce, PlanService) ->
  render = ->
    PlanService.all().then (result) ->
      $scope.offerings = result.offerings
      $scope.terms = result.terms

  render()

  $scope.toggleTerm = (term) =>
    term.toggle()

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

CourseDialogController = ($scope, $mdDialog) ->
  $scope.toggleEnroll = (offering) ->
    offering.toggleEnroll()
    $mdDialog.hide(offering.id)

  $scope.cancel = ->
    $mdDialog.cancel()

dartplanApp.controller 'SearchController', ['$rootScope', '$scope', '$mdDialog', 'SearchService', ($rootScope, $scope, $mdDialog, SearchService) ->
  $scope.fields = {}

  $scope.submit = ->
    $scope.loading = true
    SearchService.search($scope.fields).then (courses) ->
      $scope.courses = courses
      $scope.loading = false
]

dartplanApp.directive 'courseSearchResult', ['$mdDialog', 'SearchService', ($mdDialog, SearchService) ->
  return {
    replace: true,
    templateUrl: 'static/partials/course-search-result.html',
    controller: ($scope) ->
      $scope.showTermModal = (course) ->
        $scope.offeringsLoading = true
        SearchService.get_course_offerings(course.id).then (offerings) ->
          $scope.offerings = offerings
          $scope.offeringsLoading = false

        $mdDialog.show({
          controller: CourseDialogController,
          scope: $scope,
          preserveScope: true,
          templateUrl: 'static/partials/course-dialog.html',
          clickOutsideToClose: true
        })
  }
]
