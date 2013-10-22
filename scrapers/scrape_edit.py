#!../flask/bin/python

# scrape_edit.py
# Alex Gerstein
# Main file to do whatever
# garbage is necessary to fix
# the scraping errors

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

# Add current timetable, usurping any previous new entries
scrape_timetable()

# If course in database was not added by the latest scraping, then it has been changed by the registrar. So, delete.
if (curr_orc_shortcut == "") and (old_orcs_shortcut == ""):
	remove_deleted_offerings()