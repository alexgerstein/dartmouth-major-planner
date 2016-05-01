dartplanApp = angular.module 'dartplanApp'

dartplanApp.factory 'Distributive', ->
  class Distributive
    constructor: (options) ->
      {@id, @abbr} = options

dartplanApp.factory 'DistributivesService', ['$http', 'Distributive', ($http, Distributive) ->
  new class Distributives
    getAll: ->
      $http.get("/api/distributives").then (result) ->
        new Distributive distributive for distributive in result.data.distributives
]
