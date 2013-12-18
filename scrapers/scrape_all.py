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
from scrape_timetable import *

# Option to debug scraping by jumping to a page
curr_orc_shortcut = ""
old_orcs_shortcut = ""

# Add missing pre-defined models to the database
# store_distribs()
store_hours()
store_terms()

# Set current range of timetable
timetable_globals = Timetable()
starting_timetable_term = Term.query.filter_by(year = timetable_globals.TIMETABLE_START_YEAR, season = timetable_globals.TIMETABLE_START_SEASON).first()
ending_timetable_term = Term.query.filter_by(year = timetable_globals.TIMETABLE_LATEST_YEAR, season = timetable_globals.TIMETABLE_LATEST_SEASON).first()

# Remove all "user added" that no user actually has anymore
# i.e. fix user error
remove_erroneous_user_adds()

# Add current ORC
scrape_curr_orc(starting_timetable_term, ending_timetable_term, curr_orc_shortcut)

# Add all old classes
scrape_old_orcs(starting_timetable_term, ending_timetable_term, old_orcs_shortcut)

# Add current timetable, usurping any previous new entries
scrape_timetable()

# If course in database was not added by the latest scraping, then it has been changed by the registrar. So, delete.
if (curr_orc_shortcut == "") and (old_orcs_shortcut == ""):
	remove_deleted_offerings(timetable_globals)