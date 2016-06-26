from tests.factories import *
from dartplan.models import Plan

from user_factories import UserFactory


class PlanFactory(BaseFactory):
    class Meta:
        model = Plan

    title = 'Default'
    user = factory.SubFactory(UserFactory)
    terms = factory.PostGenerationMethodCall('reset_terms')
    default = True

    @factory.post_generation
    def offerings(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for offering in extracted:
                self.enroll(offering)
