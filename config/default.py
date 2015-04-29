import os
import logging

basedir = os.path.abspath(os.path.dirname('manage.py'))

DEBUG = False
CSRF_ENABLED = True
SECRET_KEY = 'youll-never-guess'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True

# email server
MAIL_SERVER = 'mail.gandi.net'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

logging.basicConfig(level=logging.WARNING)

logger = logging.getLogger('DARTplan')
logger.setLevel(logging.INFO)

logger.info("Default settings loaded.")
