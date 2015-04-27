from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
offering = Table('offering', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('course_id', Integer),
    Column('term_id', Integer),
    Column('hour_id', Integer),
    Column('desc', String),
    Column('added', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['offering'].columns['desc'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['offering'].columns['desc'].create()
