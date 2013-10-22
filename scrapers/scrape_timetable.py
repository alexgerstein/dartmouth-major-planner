# scrape_timetable.py
# Alex Gerstein
# Adapted from coursetown's scraper_timetable

from scrape_functions import *

import urllib2
import bs4

timetable_url = 'winter 2013 tt.html'

SEASON_MONTH = {"01": "W", "03": "S", "06": "X", "09": "F"}

# Defined each column's value
TERM_COL = 0
DEPT_COL = 2
NUM_COL = 3
SEC_COL = 4
TITLE_COL = 5
HOUR_COL = 7

# Get the timetable's html
def url_to_html_str(url):
    # Setup the header and request settings
    txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    
    # Get the request
    req = urllib2.Request(timetable_url, None, txheaders)
    handle = urllib2.urlopen(req)
    html = handle.read() #returns the page
    return html

# Convert the html to parsable soup
def html_to_soup(html):
    soup = BeautifulSoup(html.decode("utf-8"), features="html5lib")
    print soup
    return soup

# Import the courses to the database by row 
def parse_soup(soup):
    # Narrow the page down to the table itself
    soup = soup.find('div', {'class': 'data-table'})
    soup = soup.find('tbody')

    # Get all rows, removing column headers
    rows = soup.findAll('tr')
    rows = rows[1:]

    # Look up each row's course and offering in the database.
    # Add if not in database, but all values are present
    for row in rows:
        for index, value in enumerate(row.findAll('td')):

            # Store the term of offering
            if index == TERM_COL:
                year = value.text[:4]
                season = SEASON_MONTH.get(value.text[4:])

                term = Term.query.filter_by(year = year, season = season).first()
                if term == None:
                    break
            
            # Store the department of course
            elif index == DEPT_COL:
                dept = Department.query.filter_by(abbr = value.text.strip(" ")).first()

                if dept is None:
                    break

            # Store the number of course
            elif index == NUM_COL:
                number = value.text.lstrip("0")

                if number == "":
                    number = None
                    break

            elif index == SEC_COL:
                section = value.text.lstrip("0")

                if section == "":
                    section = None
                    break


            elif index == TITLE_COL:
                title = value.text

                if title == "":
                    break

                if ("(Discussion)" in title) or ("(Laboratory)" in title):
                    break

            elif index == HOUR_COL:
                hour = value.text.replace(u'\xa0', u' ')

                period = Hour.query.filter_by(period = hour.strip(" ")).first()
                if period is None:
                    period = Hour(period = hour.strip(" "))
                    db.session.add(period)
                    db.session.commit()

        if term and dept and (number is not "") and (section is not "") and ( title is not "") and period:

            course = Course.query.filter_by(department = dept, number = number).first()
            
            # If initial search for course fails, check if it's a topics course
            if not course:
                course = Course.query.filter_by(department = dept, number = number + "." + section).first()

            # Otherwise, add the course. It's not ideal to take these course 
            # names since they're often abbreviated, but it will have to do.
            if not course:
                course = Course(department = dept.id, number = number, name = title)
                db.session.add(course)
                db.session.commit()
                print_alert("COURSE ADDED: " + str(course))
            else:
                print str(course)

            offering = Offering.query.filter_by(course = course, term = term, hour = period).first()

            if not offering:
                general_offering = Offering.query.filter_by(course = course, term = term).first()

                print "PERIOD: " + str(period)

                offering_desc = ""
                if general_offering:
                    offering_desc = general_offering.desc

                offering = Offering(course = course.id, term = term.id, hour = period.id, desc = offering_desc)
                db.session.add(offering)
                db.session.commit()
                print_alert("OFFERING ADDED: " + str(offering))
            else:
                print str(offering)
            offering.mark("F")

            # Delete all non-final offerings of the term. If they're still in 
            # the timetable, they'll be added back
            old_offerings = Offering.query.filter_by(course = course, term = term).all()
            for old_offering in old_offerings:
                if old_offering.added != "F":
                    db.session.delete(old_offering)
                    print_alert("OFFERING DELETED: " + str(offering))
            db.session.commit()



def scrape_timetable():
    html = url_to_html_str(timetable_url)
    soup = html_to_soup(html)
    parse_soup(soup)
