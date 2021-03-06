import os
import logging

SECRET_KEY = os.environ['SECRET_KEY']
WTF_CSRF_SECRET_KEY = os.environ['WTF_CSRF_SECRET_KEY']

MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_NATIVE_UNICODE = False

LOCALYTICS_APP_KEY = os.environ['LOCALYTICS_APP_KEY']
LOCALYTICS_API_KEY = os.environ['LOCALYTICS_API_KEY']
LOCALYTICS_API_SECRET = os.environ['LOCALYTICS_API_SECRET']

logger = logging.getLogger('DARTplan')
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

logger.info("Production settings loaded.")
