# scrape_edit.py
# Alex Gerstein
# File to run database fixes quickly.

# Add app directory to path
import sys
app_path = "../"
sys.path.insert(0, app_path)

from app import app

from scrape_curr_orc import *
from scrape_old_orcs import *
from scrape_timetable import *

dfsp = Hour.query.filter_by(period = "D.F.S.P").first()
if dfsp:
    dfsps = Offering.query.filter_by(hour_id = dfsp.id).all()

    fs = Hour.query.filter_by(period = "FS").first()
    for offering in dfsps:
        offering.change_period(fs)

    db.session.delete(dfsp)
    db.session.commit()

fsp = Hour.query.filter_by(period = "FSP").first()
if fsp:
    fsps = Offering.query.filter_by(hour_id = fsp.id).all()

    fs = Hour.query.filter_by(period = "FS").first()
    for offering in fsps:
        offering.change_period(fs)

    db.session.delete(fsp)
    db.session.commit()


dlsa = Hour.query.filter_by(period = "D.L.S.A").first()
if dlsa:
    dlsas = Offering.query.filter_by(hour_id = dlsa.id).all()

    ls = Hour.query.filter_by(period = "LS").first()
    for offering in dlsas:
        offering.change_period(ls)

    db.session.delete(dlsa)
    db.session.commit()


lsa = Hour.query.filter_by(period = "LSA").first()
if lsa:
    lsas = Offering.query.filter_by(hour_id = lsa.id).all()

    ls = Hour.query.filter_by(period = "LS").first()
    for offering in lsas:
        offering.change_period(ls)

    db.session.delete(lsa)
    db.session.commit()


ar = Hour.query.filter_by(period = "AR").first()
if ar:
    ars = Offering.query.filter_by(hour_id = ar.id).all()

    arrange = Hour.query.filter_by(period = "Arrange").first()
    for offering in ars:
        offering.change_period(arrange)

    db.session.delete(ar)
    db.session.commit()

