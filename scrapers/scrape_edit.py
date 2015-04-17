# scrape_edit.py
# Alex Gerstein
# File to run database fixes quickly.

from scrape_curr_orc import *
from scrape_old_orcs import *
from scrape_timetable import *
from scrape_medians import *

def scrape_edit():
    dept = Department.query.filter_by(abbr = "ANTH").first()
    offering_course  = Course.query.filter_by(department_id = dept.id, number = float(12.3)).first()

    query =  Course.query.filter(Course.number == offering_course.number, Course.department_id == offering_course.department_id, Course.name != offering_course.name, Course.name.ilike(offering_course.name + "%"))

    print query

    print offering_course
    print query.first()
