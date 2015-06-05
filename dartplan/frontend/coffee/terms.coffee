dartplanApp = angular.module 'dartplanApp'

dartplanApp.factory 'Term', ->
  class Term
    constructor: (options) ->
      {@id, @abbr, @on} = options

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
