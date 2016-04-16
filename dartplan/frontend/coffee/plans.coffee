dartplanApp = angular.module 'dartplanApp'

dartplanApp.factory 'Plan', ['Term', 'Offering', (Term, Offering) ->
  class Plan
    constructor: (options) ->
      {@title} = options
      @terms = (new Term term for term in options.terms)
      @offerings = (new Offering offering for offering in options.offerings)
]

dartplanApp.factory 'PlansService', ['$http', 'Plan', ($http, Plan) ->
  new class Plans
    getPlan: ->
      $http.get('/api/plan').then (result) ->
        new Plan result.data.plan
]
