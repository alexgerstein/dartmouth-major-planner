# scrape_department_pages.py
# Alex Gerstein

from scrape_functions import *
from datetime import date

# List of all department course description pages to scrape
# Format: URLs, Abbreviation, Name
AAAS_BASE = 'http://aaas.dartmouth.edu/'

ANTH_COURSE_PAGE = ['http://anthropology.dartmouth.edu/undergraduate/courses/course-schedule-term', "ANTH", 'Anthropology']
AAAS_COURSE_PAGE = [AAAS_BASE + '/undergraduate/courses', 'AAAS', 'African and African American Studies']

# List of all department offering calendars to scrape
ANTH_DEPARTMENT_PAGE = []

def scrape_anth_course_page(dept_abbreviation, department_course_page, lock_term_start, lock_term_end):
    # Get main content
    r = requests.get(department_course_page)
    orig_soup = BeautifulSoup(r.content, from_encoding=r.encoding)
    dept_sections = orig_soup.findAll('section', { 'class': 'dept-section' })

    department = Department.query.filter_by(abbr = dept_abbreviation).first()
    assert department

    # Loop through each course
    for term_selection in dept_sections:
        if not term_selection.find('table'):
            continue

        season, year = term_selection.find('h2').text.strip().split()
        season = SEASON_NAME[season.upper()]
        if len(year) == 2:
            year = '20' + year
        term = Term.query.filter_by(season=season, year=year).first()

        courses = term_selection.find('tbody')
        for index, tr in enumerate(courses.findAll('tr')):
            if index == 0:
                continue

            distribs = []

            for index, td in enumerate(tr.findAll('td')):
                if index == 0:
                    dept, number = td.text.split()
                    number = float(number)
                elif index == 1:
                    title = td.text.split(" (")[0]
                elif index == 4:
                    period = td.text
                elif index == 5:
                    for word in td.text.split():
                        stripped_dist = re.match(r"\b(ART|CI|INT|LIT|NW|QDS|SCI|SLA|SOC|TAS|TLA|TMV|W)\b", word)
                        if stripped_dist:
                            possible_distrib = Distributive.query.filter_by(abbr = stripped_dist.group(0)).first()
                            if possible_distrib:
                                distribs.append(possible_distrib)
                elif index == 6:
                    for word in td.text.split():
                        stripped_dist = re.match(r"\b(ART|CI|INT|LIT|NW|QDS|SCI|SLA|SOC|TAS|TLA|TMV|W)\b", word)
                        if stripped_dist:
                            possible_distrib = Distributive.query.filter_by(abbr = stripped_dist.group(0)).first()
                            if possible_distrib:
                                distribs.append(possible_distrib)

            offerings = [unicode(term), unicode(period)]
            course = Course.query.filter(Course.department == department, Course.name.ilike(title + "%"), Course.number == number).first()
            if course is None:

                course = Course(number=number, name=title,
                                department=department)

                db.session.add(course)
                db.session.commit()

            print repr(number), repr(title)

            store_offerings(offerings, course, department, distribs, courses, date.today().year, '', lock_term_start, lock_term_end)

def scrape_aaas_course_page(dept_abbreviation, department_course_page, lock_term_start, lock_term_end):
    # Get main content
    r = requests.get(department_course_page)
    orig_soup = BeautifulSoup(r.content, from_encoding=r.encoding)
    term_course_listings = orig_soup.find('div', {'class': 'entity'}).findAll('a')

    department = Department.query.filter_by(abbr = dept_abbreviation).first()
    assert department

    for term_course_link in term_course_listings:
        link = term_course_link['href']

        r = requests.get(AAAS_BASE + link)
        orig_soup = BeautifulSoup(r.content, from_encoding=r.encoding)

        course_listings = orig_soup.find('div', {'id': 'main-content'})

        # Get term from header
        full_term = course_listings.find('h1', { 'class': 'title'})
        split_term = full_term.text.split()
        if split_term[0].upper() not in SEASON_NAME:
            continue
        season = SEASON_NAME[split_term[0].upper()]
        year = split_term[1]
        term = Term.query.filter_by(season = season, year = year).first()
        assert term != None

        offerings = [unicode(term), unicode("Arrange")]

        # Search through listed courses by bolded headers
        # ***EXTREMELY FLAKY, but don't have any choice***
        for course_view in course_listings.findAll('article', {'class': 'dept-landing-module'}):
            split_header = course_view.find('h2')
            if not split_header:
                continue
            dept_and_number = split_header.text.split()
            dept = dept_and_number[0]
            try:
                number = float(dept_and_number[1].split("-")[0])
            except:
                continue

            title = course_view.find('h3').text

            course = Course.query.filter(Course.department == department, Course.name.ilike(title + "%"), Course.number == number).first()
            if course is None:

                course = Course(number=number, name=title, department=department)

                db.session.add(course)
                db.session.commit()

            distribs = []

            desc_and_distrib_text = course_view.findAll('p')

            desc = desc_and_distrib_text[0]
            if len(desc_and_distrib_text) > 1:
                distrib_text = desc_and_distrib_text[1].text.split()

                for word in distrib_text:
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
