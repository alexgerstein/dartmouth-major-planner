from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta = MetaData(bind=migrate_engine)
    hour = Table('hour', meta, autoload=True)
    hour.c.period.alter(type=VARCHAR(length=150))


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta = MetaData(bind=migrate_engine)
    hour = Table('hour', meta, autoload=True)
    hour.c.period.alter(type=VARCHAR(length=150))
