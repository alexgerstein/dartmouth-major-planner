import factory
from factory import alchemy

from dartplan.database import db

from datetime import datetime


class BaseFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session
