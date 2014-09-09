# scrape_medians.py
# Alex Gerstein

from scrape_functions import *
from bs4 import Comment

MEDIAN_BASE_URL = 'http://www.dartmouth.edu/'
MEDIAN_INDEX_URL = '~reg/transcript/medians/'

MEDIANS = {'A': 4.00, 'B': 3.00, 'C': 2.00, 'D': 1.00, 'E': 0.00,
            '+': 0.33, '-': -0.33}

def fix_dept_abbr(abbr):
    if abbr == "M&SS":
        return "MSS"

    if abbr == "LATS":
        return "LACS"

    return abbr

def store_offering_median(offering_row):
    term = None
    dept = None
    course = None
    offering = None

    for index, item in enumerate(offering_row.find_all('td')):

        text_repr = item.text

        # Term
        if index == 0:
            year = '20' + text_repr[:2]
            season = text_repr[2].upper()

            term = Term.query.filter_by(year = year, season = season).first()

        # Course
        if index == 1:
            course_text_split = text_repr.split('-')

            # Dept
            dept_abbr = course_text_split[0].strip()
            fixed_dept_abbr = fix_dept_abbr(dept_abbr)
            dept = Department.query.filter_by(abbr = fixed_dept_abbr).first()

            # Number
            number = course_text_split[1].lstrip('0').split('.')[0]
            section = course_text_split[2].lstrip('0').strip('.')
            section_number = number + "." + section

            # Try offering as section
            course = Course.query.filter_by(number = section_number, department = dept).first()
            offering = Offering.query.filter_by(course = course, term = term ).first()

            # If that fails, try as main course
            if not offering:
                course = Course.query.filter_by(number = number, department = dept).first()
                term_offerings = Offering.query.filter_by(course = course, term = term ).all()
                if len(term_offerings) >= int(section):
                    offering = term_offerings[int(section) - 1]
                elif term_offerings:
                    offering = term_offerings[0]

            if not offering:
                break

        # Add Median
        if index == 3:
            median = text_repr.replace(" ", "")

            print term, offering, offering.hour, ": ", median

            offering.median = median
            db.session.commit()

def store_term_medians(link):
    r = requests.get(MEDIAN_BASE_URL + link)
    orig_soup = BeautifulSoup(r.content, from_encoding=r.encoding)

    table = orig_soup.find('div', {'class': 'b6'}).find('tbody')

    for offering in table.find_all('tr'):
        store_offering_median(offering)

def store_medians(links):
    for link in links:
        store_term_medians(link)

def get_median_links():
    r = requests.get(MEDIAN_BASE_URL + MEDIAN_INDEX_URL)
    orig_soup = BeautifulSoup(r.content, from_encoding=r.encoding)
    return [a['href'] for a in orig_soup.find("div", {'class': 'b6'} ).find('tr').find_all('a')]

def convert_median_to_float(string_median):
    if string_median is None:
        return None

    split_median = string_median.split("/")

    if len(split_median) == 1:
        string_median = split_median[0]
        grade = 0
        for index in range(len(string_median)):
            grade += MEDIANS[string_median[index]]
        return grade

    elif len(split_median) == 2:
        float_median =  (convert_median_to_float(split_median[0]) + convert_median_to_float(split_median[1])) / 2.0
        return float_median

    else:
        return None

def convert_median_to_string(float_median):
    if float_median is None:
        return None

    if float_median >= 3.9175:
        return "A"
    elif float_median >= 3.7525:
        return "A/A-"
    elif float_median >= 3.585:
        return "A-"
    elif float_median >= 3.415:
        return "A-/B+"
    elif float_median >= 3.2475:
        return "B+"
    elif float_median >= 3.0825:
        return "B+/B"
    elif float_median >= 2.9175:
        return "B"
    elif float_median >= 2.7525:
        return "B/B-"
    elif float_median >= 2.585:
        return "B-"
    elif float_median >= 2.415:
        return "B-/C+"
    elif float_median >= 2.2475:
        return "C+"
    elif float_median >= 2.0825:
        return "C+/C"
    elif float_median >= 1.9175:
        return "C"
    elif float_median >= 1.7525:
        return "C/C-"
    elif float_median >= 1.5875:
        return "C-"
    elif float_median >= 1.4225:
        return "C-/D+"
    elif float_median >= 1.2575:
        return "D+"
    elif float_median >= 1.0925:
        return "D+/D"
    elif float_median >= 0.9275:
        return "D"
    elif float_median >= 0.7625:
        return "D/D-"
    elif float_median >= 0.5975:
        return "D-"
    elif float_median >= 0.4325:
        return "D-/E+"
    elif float_median >= 0.2675:
        return "E+"
    elif float_median >= 0.1025:
        return "E+/E"
    else:
        return "E"

def calculate_course_medians():
    courses = Course.query.all()

    for course in courses:
        print course
        numeric_medians = map(lambda x: convert_median_to_float(x.median), course.offerings)
        numeric_medians = filter(lambda x: x != None, numeric_medians)
        sort_medians = sorted(numeric_medians)

        median_count = len(sort_medians)

        if median_count == 0:
            course.avg_median = ""

        # Odd
        elif median_count % 2 != 0:
            avg_median_float = sort_medians[median_count / 2]
            course.avg_median = convert_median_to_string(avg_median_float)

        # Even
        elif len(sort_medians) % 2 == 0:
            avg_median_float = (sort_medians[median_count / 2 - 1] + sort_medians[median_count / 2]) / 2.0
            course.avg_median = convert_median_to_string(avg_median_float)

        print course.avg_median

        db.session.commit()

def scrape_medians():
    median_links = get_median_links()
    store_medians(median_links)
    calculate_course_medians()
