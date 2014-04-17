from flask import Flask, Blueprint, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask_cas import flask_cas
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

# __init__.py
# Alex Gerstein
# Initialize the Flask app according to config, views, and models

app = Flask(__name__)
app.config.from_object('config')

if not app.debug:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('DartPlan startup')


from emails import mail
emails.mail.init_app(app)

app.register_blueprint(flask_cas)

app.jinja_env.add_extension('jinja2.ext.loopcontrols')

db = SQLAlchemy(app, session_options={'expire_on_commit':False})


from app import views, models

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

admin = Admin(app)
admin.add_view(UserView(models.User, db.session))
admin.add_view(ModelViewWithoutCreate(models.Course, db.session))
admin.add_view(OfferingView(models.Offering, db.session))

