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

dept = Department.query.filter_by(abbr = "COSC").first()
print dept

course = Course.query.filter_by(department = dept, number = "76").first()
print course

term = Term.query.filter_by(season = "W", year = "2014").first()
print term

offering = Offering.query.filter_by(course = course, term = term).first()
print offering

print User.query.filter(User.courses.contains(offering)).count()