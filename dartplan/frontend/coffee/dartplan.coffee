dartplanApp = angular.module 'dartplanApp', ['ngRoute', 'ngMaterial', 'ngMdIcons']

class config
  constructor: ($httpProvider, $routeProvider, $locationProvider, $interpolateProvider, $mdThemingProvider) ->
    $httpProvider.defaults.headers
      .common['X-CSRF-Token'] = $('meta[name=csrf-token]').attr('content');

    $routeProvider.
    when("/plans/:id",
      {
        templateUrl: '/static/partials/planner.html',
        controller: 'MainController'
      }
    ).
    when("/about",
      {
        templateUrl: '/static/partials/about.html',
        controller: 'MainController'
      }
    ).
    when("/disclaimer",
      {
        templateUrl: '/static/partials/disclaimer.html',
        controller: 'MainController'
      }
    ).
    when('/index',
      {
        templateUrl: '/static/partials/index.html',
        controller: 'MainController'
      }
    ).
    when('/',
      {
        redirectTo: '/index',
        controller: 'MainController'
      }
    ).
    otherwise(
      {
        templateUrl: '/static/partials/404.html'
        controller: 'MainController'
      }
    )

    $locationProvider.html5Mode({
      enabled: true,
      requireBase: false
    })

    $interpolateProvider
      .startSymbol '{['
      .endSymbol ']}'

    $mdThemingProvider.theme 'default'
      .primaryPalette 'green'
      .accentPalette 'amber'
      .warnPalette 'indigo'



dartplanApp.config config
