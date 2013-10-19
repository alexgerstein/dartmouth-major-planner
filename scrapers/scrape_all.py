#!../flask/bin/python
# Add app directory to path
import sys
app_path = "../"
sys.path.insert(0, app_path)

from app import app

from scrape_curr_orc import *
from scrape_old_orcs import *

# Add missing pre-defined models to the database
store_distribs()
store_hours()
store_terms()

# Add current ORC
scrape_curr_orc()

# Add all old classes
scrape_old_orcs()

# If course in database was not added by the latest scraping, then it has been changed by the registrar. So, delete.
remove_deleted_offerings()