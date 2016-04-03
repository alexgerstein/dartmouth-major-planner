dartplanApp = angular.module 'dartplanApp', ['ngMaterial', 'ngMdIcons']

class config
  constructor: ($httpProvider, $interpolateProvider, $mdThemingProvider) ->
    $httpProvider.defaults.headers
      .common['X-CSRF-Token'] = $('meta[name=csrf-token]').attr('content');

    $interpolateProvider
      .startSymbol '{['
      .endSymbol ']}'

    $mdThemingProvider.theme 'default'
      .primaryPalette 'green'
      .accentPalette 'amber'

dartplanApp.config config
