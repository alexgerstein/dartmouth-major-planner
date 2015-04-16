from flask import g
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

from dartplan.database import db
from dartplan.models import User, Course, Offering


class ViewWithValidation(ModelView):
    def is_accessible(self):
        return g.user.netid == 'd36395d'


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
