#!flask/bin/python
# db_trash.py
# Recipe to remove an entire database.
# LITERALLY THE ENTIRE DATABASE!!!!
# USE WITH CAUTION

from sqlalchemy.engine import reflection
from sqlalchemy import create_engine
from sqlalchemy.schema import (
    MetaData,
    Table,
    DropTable,
    ForeignKeyConstraint,
    DropConstraint,
    )
from config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

conn = engine.connect()

# the transaction only applies if the DB supports
# transactional DDL, i.e. Postgresql, MS SQL Server
trans = conn.begin()

inspector = reflection.Inspector.from_engine(engine)

# gather all data first before dropping anything.
# some DBs lock after things have been dropped in 
# a transaction.

metadata = MetaData()

tbs = []
all_fks = []

for table_name in inspector.get_table_names():
    fks = []
    for fk in inspector.get_foreign_keys(table_name):
        if not fk['name']:
            continue
        fks.append(
            ForeignKeyConstraint((),(),name=fk['name'])
            )
    t = Table(table_name,metadata,*fks)
    tbs.append(t)
    all_fks.extend(fks)

for fkc in all_fks:
    conn.execute(DropConstraint(fkc))

for table in tbs:
    conn.execute(DropTable(table))

trans.commit()