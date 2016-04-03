from dartplan.forms import UserEditForm


class TestUserEditForm:
    """Register form."""

    def test_validate_success(self, user):
        """Enter username that is already registered."""
        form = UserEditForm(obj=user)
        assert form.validate() is True
