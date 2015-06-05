dartplanApp = angular.module 'dartplanApp'

dartplanApp.directive 'courseSearchResult', ->
  return {
    replace: true,
    templateUrl: 'static/partials/course-search-result.html',
    controller: CourseDialogLauncherController
  }

dartplanApp.directive 'termOffering', ->
  return {
    replace: true,
    templateUrl: 'static/partials/term-offering.html',
    controller: CourseDialogLauncherController
  }
