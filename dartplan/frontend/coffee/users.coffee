dartplanApp = angular.module 'dartplanApp'

dartplanApp.factory 'User', ->
  class User
    constructor: (options) ->
      {@id, @nickname, @netid, @email, @grad_year, @is_pro, @email_course_updates, @email_Dartplan_updates} = options

    class_year: ->
      @grad_year % 100

dartplanApp.factory 'UsersService', ['$http', 'User', ($http, User) ->
  new class Users
    get: ->
      $http.get('/api/user').then (result) ->
        user = new User result.data.user
        ll('setCustomerId', user.netid)
        ll('setCustomerName', user.nickname)
        ll('setCustomerEmail', user.email)
        user
]
