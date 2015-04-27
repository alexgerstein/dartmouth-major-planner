import logging

SECRET_KEY = os.environ['SECRET_KEY']

# email server
MAIL_SERVER = 'mail.gandi.net'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_NATIVE_UNICODE = False

logger = logging.getLogger('DARTplan')
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

logger.info("Production settings loaded.")
