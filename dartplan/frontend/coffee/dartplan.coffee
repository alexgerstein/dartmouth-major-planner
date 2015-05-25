angular.module 'dartplanApp', ['ngMaterial', 'ngMdIcons']

class config
  constructor: ($interpolateProvider, $mdThemingProvider) ->
    $interpolateProvider
      .startSymbol '{['
      .endSymbol ']}'

    $mdThemingProvider.theme 'default'
      .primaryPalette 'green'
      .accentPalette 'orange'

angular.module('dartplanApp').config config
