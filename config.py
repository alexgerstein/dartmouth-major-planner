import os
basedir = os.path.abspath(os.path.dirname(__file__))

APP_NAME = 'DartmouthCoursePicker'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'youll-never-guess'

# CAS Authentication
CAS_URL = 'https://login.dartmouth.edu/cas/'