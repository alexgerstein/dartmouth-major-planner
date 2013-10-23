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

timetable_url = 'http://oracle-www.dartmouth.edu/dart/groucho/timetable.display_courses?subjectradio=allsubjects&depts=no_value&periods=no_value&distribs=no_value&distribs_i=no_value&distribs_wc=no_value&pmode=public&term=&levl=&fys=n&wrt=n&pe=n&review=n&crnl=no_value&classyear=2008&searchtype=General+Education+Requirements&termradio=allterms&terms=no_value&distribradio=alldistribs&hoursradio=allhours&sortorder=dept'

def scrape_W13():
    html = url_to_html_str(timetable_url)
    soup = html_to_soup(html)
    parse_soup(soup)