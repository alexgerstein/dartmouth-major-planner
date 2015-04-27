from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
term = Table('term', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('year', SmallInteger),
    Column('season', String(length=15)),
    Column('user_id', Integer),
    Column('off_user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['term'].columns['off_user_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['term'].columns['off_user_id'].drop()
