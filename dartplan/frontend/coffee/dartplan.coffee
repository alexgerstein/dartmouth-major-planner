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

dartplanApp.factory 'Offering', ['$http', 'Term', ($http, Term) ->
  class Offering
    constructor: (options) ->
      {@id, @name} = options
      @term = options.term.abbr
]

dartplanApp.factory 'Term', ['$http', ($http) ->
  class Term
    constructor: (options) ->
      {@id, @abbr} = options
]

dartplanApp.factory 'Course', ['$http', ($http) ->
  class Course
    constructor: (options) ->
      {@id, @full_name} = options
]

dartplanApp.controller 'PlannerController', ['$scope', 'PlanService', ($scope, PlanService) ->
  PlanService.all().then (result) ->
    $scope.offerings = result.offerings
    $scope.terms = result.terms
]

dartplanApp.controller 'SearchController', ['$scope', 'SearchService', ($scope, SearchService) ->
  $scope.fields = {}

  $scope.submit = ->
    $scope.loading = true
    SearchService.search($scope.fields).then (courses) ->
      $scope.courses = courses
      $scope.loading = false
]
