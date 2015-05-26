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

dartplanApp.factory 'SearchService', ['$http', 'Course', ($http, Course) ->
  new class Search
    search: (options) ->
      $http.get('/api/courses', {params: options}).then (result) ->
        new Course course for course in result.data.courses
]

dartplanApp.factory 'Term', ['$http', ($http) ->
  class Term
    constructor: (options) ->
      {@id, @abbr} = options
]

dartplanApp.factory 'Offering', ['$http', '$rootScope', '$mdToast', 'Term', ($http, $rootScope, $mdToast, Term) ->
  class Offering
    constructor: (options) ->
      {@id, @name, @enrollment} = options
      @term = new Term options.term

    enroll: ->
      $http.put("/api/offerings/#{ @id }", {enrolled: true}).then (result) ->
        $rootScope.$broadcast 'changedCourses'
        $mdToast.showSimple('Enroll Successful');

]

dartplanApp.factory 'Course', ['$http', 'Offering', ($http, Offering) ->
  class Course
    constructor: (options) ->
      {@id, @full_name} = options

    offerings: ->
      $http.get("/api/courses/#{ @id }/offerings").then (result) =>
        new Offering offering for offering in result.data.offerings
]

dartplanApp.controller 'PlannerController', ['$scope', 'PlanService', ($scope, PlanService) ->
  PlanService.all().then (result) ->
    $scope.offerings = result.offerings
    $scope.terms = result.terms

  $scope.$on 'changedCourses', ->
    PlanService.all().then (result) ->
      $scope.offerings = result.offerings
      $scope.terms = result.terms
]

CourseDialogController = ($scope, $mdDialog) ->
  $scope.offeringsLoading = true

  $scope.course.offerings().then (offerings) ->
    $scope.offerings = offerings
    $scope.offeringsLoading = false

  $scope.enroll = (offering) ->
    offering.enroll()
    $mdDialog.hide()

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

dartplanApp.directive 'courseSearchResult', ['$mdDialog', ($mdDialog) ->
  return {
    replace: true,
    templateUrl: 'static/partials/course-search-result.html',
    controller: ($scope) ->
      $scope.showCourseTerms = ->
        $mdDialog.show({
          controller: CourseDialogController,
          scope: $scope,
          preserveScope: true,
          templateUrl: 'static/partials/course-dialog.html',
          clickOutsideToClose: true
        })
  }
]
