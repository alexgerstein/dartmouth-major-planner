#!../flask/bin/python

# scrape_W13.py
# Alex Gerstein
# Main file to scrape W13. The term that was
# removed while I was working on this webapp.

# Add app directory to path
import sys
app_path = "../"
sys.path.insert(0, app_path)

from app import app

from scrape_timetable import *


# Add missing pre-defined models to the database
# store_distribs()
store_hours()
store_terms()

timetable_url = 'https://raw.github.com/alexgerstein/dartmouth-major-planner/master/scrapers/W2013.html'

html = url_to_html_str(timetable_url)
soup = html_to_soup(html)
parse_soup(soup)