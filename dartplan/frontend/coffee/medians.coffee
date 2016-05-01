dartplanApp = angular.module 'dartplanApp'

dartplanApp.factory 'Median', ->
  class Median
    constructor: (options) ->
      {@id, @value} = options

dartplanApp.factory 'MediansService', ['$http', 'Median', ($http, Median) ->
  new class Medians
    getAll: ->
      $http.get("/api/medians").then (result) ->
        new Median median for median in result.data.medians
]
