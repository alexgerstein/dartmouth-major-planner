dartplanApp = angular.module 'dartplanApp'

dartplanApp.factory 'User', ->
  class User
    constructor: (options) ->
      {@nickname, @grad_year, @email_course_updates, @email_Dartplan_updates} = options

    class_year: ->
      @grad_year % 100

dartplanApp.factory 'UsersService', ['$http', 'User', ($http, User) ->
  new class Users
    get: ->
      $http.get('/api/user').then (result) ->
        new User result.data.user
]
