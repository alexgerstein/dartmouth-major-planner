import os
import logging

SECRET_KEY = os.environ['SECRET_KEY']

MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_NATIVE_UNICODE = False

logger = logging.getLogger('DARTplan')
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

logger.info("Production settings loaded.")
