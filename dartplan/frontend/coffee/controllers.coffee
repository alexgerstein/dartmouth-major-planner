dartplanApp = angular.module 'dartplanApp'

dartplanApp.controller 'MainController', ['$scope', '$route', '$location', '$routeParams', 'PlansService', 'UsersService', ($scope, $route, $location, $routeParams, PlansService, UsersService) ->
  $scope.planLoaded = false

  $scope.getPlan = ->
    return unless $scope.plan_id
    PlansService.getPlan($scope.plan_id).then (plan) ->
      $scope.plan = plan
      $scope.planLoaded = true

  $scope.getCurrentUser = ->
    UsersService.get().then (user) ->
      $scope.user = user

  $scope.isCurrentUser = ->
    $scope.user and $scope.plan and $scope.plan.user.id == $scope.user.id

  $scope.isProUser = ->
    $scope.user and $scope.user.is_pro

  $scope.$route = $route
  $scope.plan_id = $routeParams.id
  $scope.getPlan()
  $scope.getCurrentUser()
  ll('tagScreen', $route.current.originalPath)
]

dartplanApp.controller 'SettingsController', ['$scope', 'PlansService', ($scope, PlansService) ->

  $scope.toggleFifthYear = (plan) =>
    PlansService.toggleFifthYear(plan.id, !plan.fifth_year)

  $scope.saveTitle = (plan) =>
    PlansService.saveTitle(plan.id, plan.title)

  $scope.checkSubmit = (e) =>
    if e.which == 13
      e.target.blur()
]

dartplanApp.controller 'PlansController', ['$scope', '$mdDialog', '$location', 'PlansService', ($scope, $mdDialog, $location, PlansService) ->
  $scope.showNewPlanDialog = ->
    if $scope.isProUser() || ($scope.user.number_of_plans == 0)
      $mdDialog.show({
        controller: NewPlanDialogController,
        scope: $scope,
        preserveScope: true,
        templateUrl: '/static/partials/new-plan-dialog.html',
        clickOutsideToClose: true
      })
    else
      $location.path('/pro')

  $scope.setAsDefault = (plan_id) ->
    PlansService.setAsDefault(plan_id).then (plan) ->
      $scope.default_plan_id = plan.id

  $scope.get_plans = ->
    PlansService.getPlans().then (plans) ->
      for plan in plans
        $scope.default_plan_id = plan.id if plan.default
      $scope.plans = plans

  $scope.get_plans()
]

dartplanApp.controller 'PlannerController', ['$scope', '$mdDialog', '$sce', 'PlansService', 'TermsService', ($scope, $mdDialog, $sce, PlansService, TermsService) ->
  render = ->
    $scope.getPlan()

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

NewPlanDialogController = ($scope, $mdDialog, $location, PlansService) ->
  $scope.cancel = ->
    $mdDialog.cancel()

  $scope.createNewPlan = ->
    PlansService.createPlan($scope.new_plan_title, $scope.new_plan_fifth_year).then (plan) ->
      $mdDialog.cancel()
      $location.path('/plans/' + plan.id)

CourseDialogController = ($scope, $mdDialog, OfferingsService, TermsService, course, plan_id) ->
  $scope.custom = {}
  $scope.course = course
  $scope.plan_id = plan_id
  $scope.offeringsLoading = true
  $scope.customTermsLoading = true
  OfferingsService.getCourseOfferings(plan_id, $scope.course.id).then (offerings) ->
    $scope.offerings = offerings
    $scope.offeringsLoading = false

  TermsService.getPlanTerms($scope.plan_id).then (terms) ->
    $scope.customUserTerms = terms
    $scope.customTermsLoading = false

  $scope.toggleEnroll = (plan_id, offering) ->
    offering.enrolled = !offering.enrolled
    if offering.user_added and offering.enrolled
      OfferingsService.enrollCustomOffering(plan_id, offering.course.id, offering.term.id).then (offering) ->
        $mdDialog.cancel()
    else
      OfferingsService.toggle(plan_id, offering.id, offering.enrolled).then (offering) ->
        $mdDialog.cancel()

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

  render = ->
    getTermOptions()
    HoursService.getAll().then (hours) ->
      $scope.hour_options = hours
    MediansService.getAll().then (medians) ->
      $scope.median_options = medians
    DepartmentsService.getAll().then (departments) ->
      $scope.department_options = departments
    DistributivesService.getAll().then (distributives) ->
      $scope.distributive_options = distributives

  getTermOptions = ->
    TermsService.getPlanTerms($scope.plan_id).then (terms) ->
      $scope.term_options = terms

  render()

  $scope.$on 'changedTerms', =>
    getTermOptions()

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
