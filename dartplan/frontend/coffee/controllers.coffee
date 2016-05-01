dartplanApp = angular.module 'dartplanApp'

dartplanApp.controller 'MainController', ['$scope', '$route', '$location', '$routeParams', ($scope, $route, $location, $routeParams) ->
  $scope.plan_id = $routeParams.id
]

dartplanApp.controller 'PlannerController', ['$scope', '$mdDialog', '$sce', 'PlansService', 'TermsService', ($scope, $mdDialog, $sce, PlansService, TermsService) ->

  render = ->
    PlansService.getPlan($scope.plan_id).then (plan) ->
      $scope.plan = plan

  render()

  $scope.toggleTerm = (term) =>
    TermsService.toggle($scope.plan_id, term.id, !term.on)

  $scope.$on 'changedCourses', =>
    render()

  $scope.showOfferingInfoModal = (offering) ->
    $scope.offering = offering
    $scope.info_html = $sce.trustAsHtml(offering.info)
    $mdDialog.show({
          controller: OfferingInfoDialogController,
          scope: $scope,
          preserveScope: true,
          templateUrl: '/static/partials/offering-info-dialog.html',
          clickOutsideToClose: true
        })
]

OfferingInfoDialogController = ($scope, $mdDialog) ->
  $scope.cancel = ->
    $mdDialog.cancel()

CourseDialogController = ($scope, $mdDialog, OfferingsService, TermsService, course, plan_id) ->
  $scope.custom = {}
  $scope.course = course
  $scope.plan_id = plan_id
  $scope.offeringsLoading = true
  $scope.customTermsLoading = true
  OfferingsService.getCourseOfferings($scope.course.id).then (offerings) ->
    $scope.offerings = offerings
    $scope.offeringsLoading = false

  TermsService.getPlanTerms($scope.plan_id).then (terms) ->
    $scope.customUserTerms = terms
    $scope.customTermsLoading = false

  $scope.toggleEnroll = (plan_id, offering) ->
    offering.enrolled = !offering.enrolled
    if offering.user_added and offering.enrolled
      OfferingsService.enrollCustomOffering(plan_id, offering.course.id, offering.term.id)
    else
      OfferingsService.toggle(plan_id, offering.id, offering.enrolled)

  $scope.enrollCustomOffering = (plan_id) ->
    existingOffering = ($scope.offerings.filter (i) -> i.term.id.toString() is $scope.custom.term_id)[0]

    if existingOffering and !existingOffering.user_added
      $scope.toggleEnroll(plan_id, existingOffering)
    else
      OfferingsService.enrollCustomOffering(plan_id, $scope.course.id, $scope.custom.term_id).then (offering) ->
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
      locals: { course: course, plan_id: $scope.plan_id },
      preserveScope: true,
      templateUrl: '/static/partials/course-dialog.html',
      clickOutsideToClose: true
    })

dartplanApp.controller 'SearchController', ['$rootScope', '$scope', '$mdDialog', 'TermsService', 'HoursService', 'DepartmentsService', 'DistributivesService', 'MediansService', 'CourseService',  ($rootScope, $scope, $mdDialog, TermsService, HoursService, DepartmentsService, DistributivesService, MediansService, CourseService) ->
  $scope.fields = {}

  TermsService.getPlanTerms($scope.plan_id).then (terms) ->
    $scope.term_options = terms
  HoursService.getAll().then (hours) ->
    $scope.hour_options = hours
  MediansService.getAll().then (medians) ->
    $scope.median_options = medians
  DepartmentsService.getAll().then (departments) ->
    $scope.department_options = departments
  DistributivesService.getAll().then (distributives) ->
    $scope.distributive_options = distributives

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
