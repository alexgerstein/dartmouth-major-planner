import os
import logging

basedir = os.path.abspath(os.path.dirname('manage.py'))

TESTING = True
WTF_CSRF_ENABLED = False
LOGIN_DISABLED = False
SQLALCHEMY_DATABASE_URI = ('sqlite:///:memory:')

logger = logging.getLogger('DARTplan')
logger.info("Testing settings loaded.")
