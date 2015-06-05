dartplanApp = angular.module 'dartplanApp'

dartplanApp.controller 'PlannerController', ['$scope', '$mdDialog', '$sce', 'TermsService', 'OfferingsService', ($scope, $mdDialog, $sce, TermsService, OfferingsService) ->

  render = ->
    $scope.term = []
    $scope.offerings = []

    TermsService.getUserTerms().then (terms) ->
      $scope.terms = terms

    OfferingsService.getEnrolled().then (offerings) ->
      $scope.offerings = offerings

  render()

  $scope.toggleTerm = (term) =>
    TermsService.toggle(term.id, !term.on)

  $scope.$on 'changedCourses', =>
    render()

  $scope.showOfferingInfoModal = (offering) ->
    $scope.offering = offering
    $scope.info_html = $sce.trustAsHtml(offering.info)
    $mdDialog.show({
          controller: OfferingInfoDialogController,
          scope: $scope,
          preserveScope: true,
          templateUrl: 'static/partials/offering-info-dialog.html',
          clickOutsideToClose: true
        })
]

OfferingInfoDialogController = ($scope, $mdDialog) ->
  $scope.cancel = ->
    $mdDialog.cancel()

CourseDialogController = ($scope, $mdDialog, OfferingsService) ->
  $scope.toggleEnroll = (offering) ->
    OfferingsService.toggle(offering.id, !offering.enrolled)
    $mdDialog.hide()

  $scope.enrollCustomOffering = ->
    OfferingsService.enrollCustomOffering($scope.course.id, $scope.custom.term_id)
    $mdDialog.hide()

  $scope.cancel = ->
    $mdDialog.cancel()

CourseDialogLauncherController = ($scope, $mdDialog, OfferingsService, TermsService) ->
  $scope.custom = {}

  $scope.showTermModal = (course) ->
    $scope.course = course
    $scope.offeringsLoading = true
    $scope.customTermsLoading = true
    OfferingsService.getCourseOfferings(course.id).then (offerings) ->
      $scope.offerings = offerings
      $scope.offeringsLoading = false

    TermsService.getUserTerms().then (terms) ->
      $scope.customUserTerms = terms
      $scope.customTermsLoading = false

    $mdDialog.show({
      controller: CourseDialogController,
      scope: $scope,
      preserveScope: true,
      templateUrl: 'static/partials/course-dialog.html',
      clickOutsideToClose: true
    })

dartplanApp.controller 'SearchController', ['$rootScope', '$scope', '$mdDialog', 'CourseService', ($rootScope, $scope, $mdDialog, CourseService) ->
  $scope.fields = {}

  $scope.submit = ->
    $scope.loading = true
    CourseService.search($scope.fields).then (courses) ->
      $scope.courses = courses
      $scope.loading = false
]
