from flask import session, redirect, url_for, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from dartplan.database import db
from dartplan.models import User, Course, Offering


class ViewWithValidation(ModelView):
    def is_accessible(self):
        user = session.get('user')
        return user and user.get('netid') == 'd36395d'

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('flask_cas.login', next=request.url))


class ModelViewWithoutCreate(ViewWithValidation):
    can_create = False


class UserView(ModelViewWithoutCreate):
    column_searchable_list = ('netid', 'full_name')


class OfferingView(ModelViewWithoutCreate):
    # Override displayed fields
    column_list = ('course', 'term', 'hour', 'user_added', 'median')

admin = Admin()
admin.add_view(UserView(User, db.session))
admin.add_view(ModelViewWithoutCreate(Course, db.session))
admin.add_view(OfferingView(Offering, db.session))
