dartplanApp = angular.module 'dartplanApp'

dartplanApp.controller 'PlannerController', ['$scope', '$mdDialog', '$sce', 'PlansService', 'TermsService', ($scope, $mdDialog, $sce, PlansService, TermsService) ->

  render = ->
    PlansService.getPlan().then (plan) ->
      $scope.plan = plan

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

CourseDialogController = ($scope, $mdDialog, OfferingsService, TermsService, course) ->

  $scope.custom = {}
  $scope.course = course;
  $scope.offeringsLoading = true
  $scope.customTermsLoading = true
  OfferingsService.getCourseOfferings($scope.course.id).then (offerings) ->
    $scope.offerings = offerings
    $scope.offeringsLoading = false

  TermsService.getPlanTerms().then (terms) ->
    $scope.customUserTerms = terms
    $scope.customTermsLoading = false

  $scope.toggleEnroll = (offering) ->
    offering.enrolled = !offering.enrolled
    if offering.user_added and offering.enrolled
      OfferingsService.enrollCustomOffering(offering.course.id, offering.term.id)
    else
      OfferingsService.toggle(offering.id, offering.enrolled)

  $scope.enrollCustomOffering = ->
    existingOffering = ($scope.offerings.filter (i) -> i.term.id.toString() is $scope.custom.term_id)[0]

    if existingOffering and !existingOffering.user_added
      $scope.toggleEnroll(existingOffering)
    else
      OfferingsService.enrollCustomOffering($scope.course.id, $scope.custom.term_id).then (offering) ->
        if !existingOffering
          $scope.offerings.push offering
        else
          existingOffering.enrolled = true

  $scope.cancel = ->
    $mdDialog.cancel()

CourseDialogLauncherController = ($scope, $mdDialog) ->
  $scope.showTermModal = (course) ->
    $mdDialog.show({
      controller: CourseDialogController,
      locals: { course: course },
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

dartplanApp.controller 'UserFormController', ['$scope', 'UsersService', ($scope, UsersService) ->
  UsersService.get().then (user) ->
    $scope.user = user
]
