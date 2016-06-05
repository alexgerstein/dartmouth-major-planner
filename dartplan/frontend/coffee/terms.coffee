dartplanApp = angular.module 'dartplanApp'

dartplanApp.factory 'Term', ->
  class Term
    constructor: (options) ->
      {@id, @abbr, @on} = options

dartplanApp.factory 'TermsService', ['$http', '$rootScope', '$mdToast', 'Term', ($http, $rootScope, $mdToast, Term) ->
  new class Terms
    getPlanTerms: (plan_id) ->
      $http.get("/api/plans/#{plan_id}/terms").then (result) ->
        new Term term for term in result.data.terms

    toggle: (plan_id, id, enrolled) ->
      $http.put("/api/plans/#{plan_id}/terms/#{ id }", {'on': enrolled}).then (result) ->
        $rootScope.$broadcast 'changedCourses'
        $mdToast.showSimple('Successfully changed term enrollment.');

        if enrolled
          ll('tagEvent', 'Term enrolled', {'plan_id': plan_id, 'term_id': id})
        else
          ll('tagEvent', 'Term unenrolled', {'plan_id': plan_id, 'term_id': id})
]
