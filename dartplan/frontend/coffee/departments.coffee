dartplanApp = angular.module 'dartplanApp'

dartplanApp.factory 'Department', ->
  class Department
    constructor: (options) ->
      {@id, @abbr} = options

dartplanApp.factory 'DepartmentsService', ['$http', 'Department', ($http, Department) ->
  new class Departments
    getAll: ->
      $http.get("/api/departments").then (result) ->
        new Department department for department in result.data.departments
]
