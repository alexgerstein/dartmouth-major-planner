dartplanApp = angular.module 'dartplanApp'

dartplanApp.directive 'courseSearchResult', ->
  return {
    replace: true,
    templateUrl: '/static/partials/course-search-result.html',
    controller: CourseDialogLauncherController
  }

dartplanApp.directive 'termOffering', ->
  return {
    replace: true,
    templateUrl: '/static/partials/term-offering.html',
    controller: CourseDialogLauncherController
  }

dartplanApp.directive 'plannerTerm', ->
  return {
    replace: true,
    templateUrl: '/static/partials/planner-term.html',
  }

dartplanApp.directive 'plannerSettings', ->
  return {
    replace: true,
    templateUrl: '/static/partials/planner-settings.html',
  }
