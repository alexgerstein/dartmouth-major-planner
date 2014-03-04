# scrape_all.py
# Alex Gerstein
# Main file to scrape all sources of course info.

# Add app directory to path
import sys
app_path = "../"
sys.path.insert(0, app_path)

from app import app

from scrape_curr_orc import *
from scrape_old_orcs import *
from scrape_department_pages import *
from scrape_timetable import *
from scrape_medians import *

# Option to debug scraping by jumping to a page
curr_orc_shortcut = ""
old_orcs_shortcut = ""

# Add missing pre-defined models to the database
# store_distribs()
store_hours()
store_terms()
store_distribs()

# Set current range of timetable
timetable_globals = Timetable()
lock_term_start = Term.query.filter_by(year = timetable_globals.ARBITRARY_OLD_YEAR, season = timetable_globals.ARBITRARY_SEASON).first()
lock_term_end = Term.query.filter_by(year = timetable_globals.TIMETABLE_LOCK_YEAR, season = timetable_globals.TIMETABLE_LOCK_SEASON).first()

# Remove all "user added" that no user actually has anymore
# i.e. fix user error
remove_erroneous_user_adds()

# Add current ORC
scrape_curr_orc(lock_term_start, lock_term_end, curr_orc_shortcut)

# Add all old classes
scrape_old_orcs(lock_term_start, lock_term_end, old_orcs_shortcut)

# Add courses from department pages
scrape_department_pages(lock_term_start, lock_term_end)

# Add current timetable, usurping any previous new entries
scrape_timetable()

# If course in database was not added by the latest scraping, then it has been changed by the registrar. So, delete.
if (curr_orc_shortcut == "") and (old_orcs_shortcut == ""):
	remove_deleted_offerings(timetable_globals)

remove_unused_model_instances()
scrape_medians()
