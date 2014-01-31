# scrape_department_pages.py
# Alex Gerstein

from scrape_functions import *

# List of all department course description pages to scrape
# Format: URLs, Abbreviation, Name
ANTH_COURSE_PAGE = [['http://dartmouth.edu/anthropology/undergraduate/course-listings', "ANTH", 'Anthropology']]

# List of all department offering calendars to scrape
ANTH_DEPARTMENT_PAGE = []

def scrape_antrhopology_course_page(department_course_page, lock_term_start, lock_term_end):
    # Get fields-items on page
    r = requests.get(url)
    orig_soup = BeautifulSoup(r.content, from_encoding=r.encoding)
    return orig_soup.find("div", class='field-items')

def scrape_anthropology_department_site(department_course_page, lock_term_start, lock_term_end):

    print scrape_anthropology_course_page(department_course_page, lock_term_start, lock_term_end)


def scrape_department_pages(lock_term_start, lock_term_end):
    scrape_anthropology_department_site(ANTH_COURSE_PAGE, lock_term_start, lock_term_end)
