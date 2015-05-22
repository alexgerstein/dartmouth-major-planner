import pytest
from dartplan.mail import *


class TestMail:

    def test_welcome_notification(self, outbox, user):
        welcome_notification(user)
        assert len(outbox) == 1
        assert "Welcome to DARTPlan!" in outbox[0].subject

    def test_updated_hour_notification(self, outbox, user, offering, hour):
        updated_hour_notification([user], offering, hour)
        assert len(outbox) == 1
        assert "Nice call!" in outbox[0].subject

    def test_swapped_course_times(self, outbox, user,
                                  offering, registrar_added_offering):
        swapped_course_times([user], offering, registrar_added_offering)
        assert len(outbox) == 1
        assert "switcheroo" in outbox[0].subject

    def test_deleted_offering_notification(self, outbox, user, offering):
        deleted_offering_notification([user], offering,
                                      offering.term, offering.hour)
        assert len(outbox) == 1
        assert "Oh no" in outbox[0].subject
