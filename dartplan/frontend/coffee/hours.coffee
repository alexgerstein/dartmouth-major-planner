dartplanApp = angular.module 'dartplanApp'

dartplanApp.factory 'Hour', ->
  class Hour
    constructor: (options) ->
      {@id, @period} = options

dartplanApp.factory 'HoursService', ['$http', 'Hour', ($http, Hour) ->
  new class Hours
    getAll: ->
      $http.get("/api/hours").then (result) ->
        new Hour hour for hour in result.data.hours
]
