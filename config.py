# -*- coding: utf8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'youll-never-guess'

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'
else:
    SQLALCHEMY_DATABASE_URI = "postgresql://162.243.241.156:49153/dartplan"
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True