# scrape_timetable.py
# Alex Gerstein
# Adapted from coursetown's scraper_timetable

from scrape_functions import *

import urllib2
import bs4

timetable_url = 'http://oracle-www.dartmouth.edu/dart/groucho/timetable.display_courses?subjectradio=allsubjects&depts=no_value&periods=no_value&distribs=no_value&distribs_i=no_value&distribs_wc=no_value&pmode=public&term=&levl=&fys=n&wrt=n&pe=n&review=n&crnl=no_value&classyear=2008&searchtype=General+Education+Requirements&termradio=allterms&terms=no_value&distribradio=alldistribs&hoursradio=allhours&sortorder=dept'
w13timetable_url = 'https://raw.github.com/alexgerstein/dartmouth-major-planner/master/scrapers/W2013.html'

# Defined each column's value
TERM_COL = 0
DEPT_COL = 2
NUM_COL = 3
SEC_COL = 4
TITLE_COL = 5
HOUR_COL = 8
WC_COL = 12
DIST_COL = 13

# Get the timetable's html
def url_to_html_str(url):
    # Setup the header and request settings
    txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

    # Get the request
    req = urllib2.Request(url, None, txheaders)
    handle = urllib2.urlopen(req)
    html = handle.read() #returns the page
    return html

# Convert the html to parsable soup
def html_to_soup(html):
    soup = BeautifulSoup(html.decode("utf-8"), features="html5lib")
    return soup

# Import the courses to the database by row
def parse_soup(soup, search_term):

    # Narrow the page down to the table itself
    soup = soup.find('div', {'class': 'data-table'})
    soup = soup.find('tbody')

    # Get all rows, storing indices of column headers
    rows = soup.findAll('tr')

    header_row = rows[0].findAll('th')
    for index, value in enumerate(header_row):
        if "Term" in value.text:
            TERM_COL = index

        elif "Subj" in value.text:
            DEPT_COL = index

        elif "Num" in value.text:
            NUM_COL = index

        elif "Sec" in value.text:
            SEC_COL = index

        elif "Title" in value.text:
            TITLE_COL = index

        elif "Period" in value.text:
            HOUR_COL = index

        elif "WC" in value.text:
            WC_COL = index

        elif "Dist" in value.text:
            DIST_COL = index

    rows = rows[1:]

    # Look up each row's course and offering in the database.
    # Add if not in database, but all values are present
    for row in rows:
        term = None
        dept = None
        section = 0
        number = None
        title = None
        hour = None
        distribs = []

        split_number = False

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

            # Store the section of the course
            elif index == SEC_COL and not split_number:
                section = value.text.lstrip("0")

                if section == "":
                    section = None
                    break

            # Store the number of course
            elif index == NUM_COL:
                number_split = value.text.lstrip("0").split(".")
                number = number_split[0]

                # Protect for section being in course number
                if len(number_split) > 1:
                    section = number_split[1].lstrip("0")
                    split_number = True

                if number == "":
                    number = None
                    break

            elif index == TITLE_COL:
                title = value.text

                if title == "":
                    break

                if ("(Discussion)" in title) or ("(Laboratory)" in title):
                    break

            elif index == HOUR_COL:
                hour = value.text.replace(u'\xa0', u' ')

                if "AR" == hour.strip(" "):
                    hour = "Arrange"

                if "F.S.P" in hour.strip(" ") \
                or "FSP" in hour.strip(" "):
                    hour = "FS"

                if "L.S.A" in hour.strip(" ") \
                or "LSA" in hour.strip(" "):
                    hour = "LS"

                period = Hour.query.filter_by(period = hour.strip(" ")).first()
                if period is None:
                    period = Hour(period = hour.strip(" "))
                    db.session.add(period)
                    db.session.commit()

            elif index == DIST_COL or index == WC_COL:
                distrib_split = value.text.split(" ")
                for distrib in distrib_split:
                    stripped_dist = re.match(r'\b(ART|CI|INT|LIT|NW|QDS|SCI|SLA|SOC|TAS|TLA|TMV|W)\b', distrib)

                    if stripped_dist:
                        possible_distrib = Distributive.query.filter_by(abbr = stripped_dist.group(0)).first()
                        if possible_distrib:
                            distribs.append(possible_distrib)


        if ((search_term == None) or (term == search_term)) and dept and (number is not None) and (section is not "") and title and ( title is not "") and period:

            course = None

            # First check if topics course
            if split_number:
                course = Course.query.filter(Course.department == dept, Course.number == float(number + "." + str(section))).first()
                if not course:
                    course = Course(department=dept,
                                    number=float(number + "." + str(section)),
                                    name=title)
                    db.session.add(course)
                    db.session.commit()
                    print_alert("COURSE ADDED: " + str(course))
                else:
                    print str(course)

            # If initial search for course fails, check if it's not a topics course
            else:
                course = Course.query.filter(Course.department == dept, Course.number == float(number)).first()

                # Check if topic in wrong column
                if not course:
                    course = Course.query.filter(Course.department == dept, Course.number == float(number + "." + str(section))).first()

                # Otherwise, add the course. It's not ideal to take these course
                # names since they're often abbreviated, but it will have to do.
                if not course:
                    course = Course(department=dept, number=float(number),
                                    name=title)
                    db.session.add(course)
                    db.session.commit()
                    print_alert("COURSE ADDED: " + str(course))
                else:
                    print str(course)

            offering = Offering.query.filter_by(course = course, term = term, hour = period).first()

            if not offering:
                general_offering = Offering.query.filter_by(course = course, term = term).first()

                offering_desc = ""
                if general_offering:
                    offering_desc = general_offering.desc

                offering = Offering(course=course, term=term, hour=period,
                                    desc=offering_desc, user_added="N")
                db.session.add(offering)
                db.session.commit()
                print_alert("OFFERING ADDED: " + str(offering) + " in " + str(term))
            else:
                print str(offering)

            offering.added = "F"

            for distrib in distribs:
                if distrib not in offering.distributives:
                    offering.distributives.append(distrib)
                    db.session.commit()

            # Mark for removal all non-final offerings of the term. If they're still in
            # the timetable, they'll be marked as F again
            old_offerings = Offering.query.filter_by(course = course, term = term).all()
            for old_offering in old_offerings:
                if old_offering.added != "F":
                    old_offering.added = ""
            db.session.commit()



def scrape_timetable():
    # Scrape full timetable
    html = url_to_html_str(timetable_url)
    soup = html_to_soup(html)
    parse_soup(soup, None)
