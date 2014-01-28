# scrape_stats.py
# Alex Gerstein
# Various scripts to generate statistics about the site.

# Add app directory to path
import sys
app_path = "../"
sys.path.insert(0, app_path)

from app import app

from scrape_curr_orc import *
from scrape_old_orcs import *
from scrape_timetable import *


# # Check DARTPlan student enrollment
# dept = Department.query.filter_by(abbr = "COSC").first()
# print dept

# course = Course.query.filter_by(department = dept, number = "76").first()
# print course

# term = Term.query.filter_by(season = "W", year = "2014").first()
# print term

# offering = Offering.query.filter_by(course = course, term = term).first()
# print offering

# print User.query.filter(User.courses.contains(offering)).count()

#
# Most popular offerings
#
print Offering.query.order_by('users').all()

#
# Check students with more than X courses
#
users = User.query.filter(User.courses.any(), User.grad_year != 2016, User.grad_year != 2017).all()
course_count = {}
for user in users:
	count = user.courses.count()
	if count in course_count:
		course_count[count] += 1
	else:
		course_count[count] = 1

print "Course Count => Frequency"
for k,v in sorted(course_count.items()):
	bar = str(k) + ": "

	for i in range(v):
		bar += "."

	print bar
