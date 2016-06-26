dartplanApp = angular.module 'dartplanApp'

dartplanApp.factory 'Plan', ['Term', 'Offering', 'User', (Term, Offering, User) ->
  class Plan
    constructor: (options) ->
      {@id, @title, @fifth_year, @default} = options
      if options.terms
        @terms = (new Term term for term in options.terms)
        @offerings = (new Offering offering for offering in options.offerings)
        @user = new User options.user
]

dartplanApp.factory 'PlansService', ['$http', '$rootScope', '$mdToast', 'Plan', ($http, $rootScope, $mdToast, Plan) ->
  new class Plans
    getPlan: (id) ->
      $http.get("/api/plans/#{id}").then (result) ->
        new Plan result.data.plan

    createPlan: (title, fifth_year) ->
      plan_details = {'title': title, 'fifth_year': fifth_year}
      $http.post('/api/plans', plan_details).then (result) ->
        ll('tagEvent', 'Created new plan')
        new Plan result.data.plan

    getPlans: ->
      $http.get("/api/plans").then (result) ->
        new Plan plan for plan in result.data.plans

    setAsDefault: (id) ->
      $http.put("/api/plans/#{id}", {'default': true}).then (result) ->
        $mdToast.showSimple('Plan set as default.');
        ll('tagEvent', 'Set plan as default')
        new Plan result.data.plan

    saveTitle: (id, title) ->
      $http.put("/api/plans/#{id}", {'title': title}).then (result) ->
        $mdToast.showSimple('New plan title saved.');
        ll('tagEvent', 'Changed plan name')
        new Plan result.data.plan

    toggleFifthYear: (id, enrolled) ->
      $http.put("/api/plans/#{id}", {'fifth_year': enrolled}).then (result) ->
        $rootScope.$broadcast 'changedCourses'
        $rootScope.$broadcast 'changedTerms'
        $mdToast.showSimple('Successfully changed fifth-year enrollment.');

        if enrolled
          ll('tagEvent', 'Fifth-year enabled', {'plan_id': id})
        else
          ll('tagEvent', 'Fifth-year disabled', {'plan_id': id})
]
