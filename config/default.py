import os
import logging

basedir = os.path.abspath(os.path.dirname('manage.py'))

DEBUG = False
WTF_CSRF_ENABLED = True
SECRET_KEY = 'youll-never-guess'
WTF_CSRF_SECRET_KEY = 'youll-never-guess'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

DATABASE_QUERY_TIMEOUT = 0.5

# email server
MAIL_SERVER = 'mail.gandi.net'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

LOCALYTICS_APP_KEY = 'someinvalidkey'
LOCALYTICS_API_KEY = 'aninvalidkey'
LOCALYTICS_API_SECRET = 'shhhhtellnoone'

logging.basicConfig(level=logging.WARNING)

logger = logging.getLogger('DARTplan')
logger.setLevel(logging.INFO)

logger.info("Default settings loaded.")
