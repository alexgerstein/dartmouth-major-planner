from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
distributive = Table('distributive', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('abbr', String(length=10)),
)

offering_distribs = Table('offering_distribs', post_meta,
    Column('offering_id', Integer),
    Column('distributive_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['distributive'].create()
    post_meta.tables['offering_distribs'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['distributive'].drop()
    post_meta.tables['offering_distribs'].drop()
