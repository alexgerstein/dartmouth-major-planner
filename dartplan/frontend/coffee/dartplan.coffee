dartplanApp = angular.module 'dartplanApp', ['ngRoute', 'ngMaterial', 'ngMdIcons']

class config
  constructor: ($httpProvider, $routeProvider, $locationProvider, $interpolateProvider, $mdThemingProvider) ->
    $httpProvider.defaults.headers
      .common['X-CSRF-Token'] = $('meta[name=csrf-token]').attr('content');

    $routeProvider.
    when("/plans/:id",
      {
        templateUrl: '/static/partials/planner.html',
        controller: 'MainController',
        controllerAs: 'main'
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
