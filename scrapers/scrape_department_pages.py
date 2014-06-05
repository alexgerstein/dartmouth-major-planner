# scrape_department_pages.py
# Alex Gerstein

from scrape_functions import *
from datetime import date

# List of all department course description pages to scrape
# Format: URLs, Abbreviation, Name
ANTH_COURSE_PAGE = ['http://dartmouth.edu/anthropology/undergraduate/course-listings', "ANTH", 'Anthropology']
AAAS_COURSE_PAGE = ['http://www.dartmouth.edu/~african/courses/', 'AAAS', 'African and African American Studies']

# List of all department offering calendars to scrape
ANTH_DEPARTMENT_PAGE = []

def scrape_anth_course_page(dept_abbreviation, department_course_page, lock_term_start, lock_term_end):
    # Get main content
    r = requests.get(department_course_page)
    orig_soup = BeautifulSoup(r.content, from_encoding=r.encoding)
    page_content = orig_soup.find('div', { 'id': 'main-content' })

    department = Department.query.filter_by(abbr = dept_abbreviation).first()
    assert department

    # Loop through each course
    for course in page_content.findAll('h3',  text=re.compile('[0-9][.].[\s]*[A-Za-z]')):
        course_view = course.parent

        header = course_view.find('h3')

        if header is None:
            continue

        split_header = header.text.split(" ")

        number = float(split_header[0].strip(".").lstrip("0"))
        title = " ".join(split_header[1:]).strip(" ")

        offering_soup = course_view.find('p')

        if offering_soup is None:
            continue

        offerings = offering_soup.text.split(" ")

        description = offering_soup.find_next_sibling('p')

        if description is None:
            continue

        distribs = []
        split_description = description.text.split(" ")
        for word in split_description:
            stripped_dist = re.match(r"\b(ART|CI|INT|LIT|NW|QDS|SCI|SLA|SOC|TAS|TLA|TMV|W)\b", word)
            if stripped_dist:
                        possible_distrib = Distributive.query.filter_by(abbr = stripped_dist.group(0)).first()
                        if possible_distrib:
                            distribs.append(possible_distrib)

        course = Course.query.filter(Course.department == department, Course.name.ilike(title + "%"), Course.number == number).first()
        if course is None:

            course = Course(number = number, name = title, department = department.id)

            db.session.add(course)
            db.session.commit()

        print repr(number), repr(title)

        store_offerings(offerings, course, department, distribs, course_view, date.today().year, course_view.prettify(), lock_term_start, lock_term_end)

def scrape_aaas_course_page(dept_abbreviation, department_course_page, lock_term_start, lock_term_end):
    # Get main content
    r = requests.get(department_course_page)
    orig_soup = BeautifulSoup(r.content, from_encoding=r.encoding)
    page_content = orig_soup.find('div', { 'class': 'b6' })

    department = Department.query.filter_by(abbr = dept_abbreviation).first()
    assert department

    # Get term from header
    full_term = page_content.find('h2', { 'style': 'text-align: center;'})
    split_term = full_term.text.split()
    season = SEASON_NAME[split_term[0].upper()]
    year = split_term[1]
    term = Term.query.filter_by(season = season, year = year).first()
    assert term != None
    print term

    # Search through listed courses by bolded headers
    # ***EXTREMELY FLAKY, but don't have any choice***
    for course_view in page_content.findAll('p'):
        split_header = course_view.find('strong')
        if not split_header:
            continue

        split_header = split_header.text.split()
        number = float(split_header[1].strip(":").split('-')[0])
        title = " ".join(split_header[2:])

        course = Course.query.filter(Course.department == department, Course.name.ilike(title + "%"), Course.number == number).first()
        if course is None:

            course = Course(number = number, name = title, department = department.id)

            db.session.add(course)
            db.session.commit()

        desc = course_view
        distribs = []

        offering_data = course_view.find('em')
        if offering_data:

            # Get offerings
            offerings = offering_data.text.split(") ")[0].split()
            offerings.insert(0, unicode(term))

            split_desc = offering_data.text.split()
            for word in split_desc:
                stripped_dist = re.match(r"\b(ART|CI|INT|LIT|NW|QDS|SCI|SLA|SOC|TAS|TLA|TMV|W)\b", word)
                if stripped_dist:
                    possible_distrib = Distributive.query.filter_by(abbr = stripped_dist.group(0)).first()
                    if possible_distrib:
                        distribs.append(possible_distrib)

            print repr(number), repr(title)
            store_offerings(offerings, course, department, distribs, course_view, date.today().year, desc.prettify(), lock_term_start, lock_term_end)


def scrape_anth_department_site(dept_abbreviation, department_course_page, lock_term_start, lock_term_end):
    scrape_anth_course_page(dept_abbreviation, department_course_page, lock_term_start, lock_term_end)

def scrape_aaas_department_site(dept_abbreviation, department_course_page, lock_term_start, lock_term_end):
    scrape_aaas_course_page(dept_abbreviation, department_course_page, lock_term_start, lock_term_end)

def scrape_department_pages(lock_term_start, lock_term_end):
    scrape_anth_department_site(ANTH_COURSE_PAGE[1], ANTH_COURSE_PAGE[0], lock_term_start, lock_term_end)
    scrape_aaas_department_site(AAAS_COURSE_PAGE[1], AAAS_COURSE_PAGE[0], lock_term_start, lock_term_end)
