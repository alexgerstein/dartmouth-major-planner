#!/usr/bin/python
from bs4 import BeautifulSoup
import requests

BASE_URL = "http://dartmouth.smartcatalogiq.com"

DEPTS = []

def print_alert(message):
	print ('\n\n')
	print '*******' + message + '*******\n'


r = requests.get(BASE_URL + "/en/2013/orc/Departments-Programs-Undergraduate")

data = r.text
orig_soup = BeautifulSoup(data)
print_alert ('GETTING DEPARTMENT LINKS')
dept_soup = ""
for link in orig_soup.find_all(id="sc-programlinks"):
	dept_soup = BeautifulSoup(str(link))


print_alert ('SCRAPING COURSE PAGES')
undergrad_course_pages = []
for link in dept_soup.find_all("a"):

	# Get unedergraduate course listing for dept
	undergrad_course_link = BeautifulSoup(requests.get(BASE_URL + link['href']).text)
	for link in undergrad_course_link.find("div", id="rightpanel"):
			new_href = BeautifulSoup(str(link)).find("a")
			if (new_href != None):
				undergrad_course_pages.append(new_href['href'])

for link in undergrad_course_pages:
	print link + '\n'

print 'Number of course pages: ' + str(len(undergrad_course_pages))