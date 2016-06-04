dartplanApp = angular.module 'dartplanApp'

dartplanApp.factory 'Plan', ['Term', 'Offering', 'User', (Term, Offering, User) ->
  class Plan
    constructor: (options) ->
      {@title, @fifth_year} = options
      @terms = (new Term term for term in options.terms)
      @offerings = (new Offering offering for offering in options.offerings)
      @user = new User options.user
]

dartplanApp.factory 'PlansService', ['$http', '$rootScope', '$mdToast', 'Plan', ($http, $rootScope, $mdToast, Plan) ->
  new class Plans
    getPlan: (id) ->
      $http.get("/api/plans/#{id}").then (result) ->
        new Plan result.data.plan

    toggleFifthYear: (id, enrolled) ->
      $http.put("/api/plans/#{id}", {'fifth_year': enrolled}).then (result) ->
        $rootScope.$broadcast 'changedCourses'
        $mdToast.showSimple('Successfully changed fifth-year enrollment.');
]
