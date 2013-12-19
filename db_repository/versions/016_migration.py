from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('netid', String(length=15)),
    Column('full_name', String(length=200)),
    Column('nickname', String(length=64)),
    Column('grad_year', SmallInteger),
    Column('email_course_updates', Boolean),
    Column('email_Dartplan_updates', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['email_Dartplan_updates'].create()
    post_meta.tables['user'].columns['email_course_updates'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['email_Dartplan_updates'].drop()
    post_meta.tables['user'].columns['email_course_updates'].drop()
