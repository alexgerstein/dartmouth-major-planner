# scrape_curr_orc.py
# Alex Gerstein

from scrape_functions import *
from bs4 import Comment

# List of all departments missed in scraping of the ORL
# Format: URLs, Abbreviation, Name
MISSED_UG_LISTINGS = [['http://dartmouth.smartcatalogiq.com/en/2013/orc/Departments-Programs-Undergraduate/Classics-Classical-Studies-Greek-Latin/LAT-Latin', 'LAT', 'Latin'], 
['http://dartmouth.smartcatalogiq.com/en/2013/orc/Departments-Programs-Undergraduate/Classics-Classical-Studies-Greek-Latin/CLST-Classical-Studies', 'CLST', 'Classical Studies'], 
['http://dartmouth.smartcatalogiq.com/en/2013/orc/Departments-Programs-Undergraduate/Classics-Classical-Studies-Greek-Latin/GRK-Greek', 'GRK', 'Greek'], 
['http://dartmouth.smartcatalogiq.com/en/2013/orc/Departments-Programs-Undergraduate/Asian-and-Middle-Eastern-Languages-and-Literatures-Arabic-Chinese-Hebrew-Japanese/ARAB-Arabic', "ARAB", "Arabic"],
['http://dartmouth.smartcatalogiq.com/en/2013/orc/Departments-Programs-Undergraduate/Asian-and-Middle-Eastern-Languages-and-Literatures-Arabic-Chinese-Hebrew-Japanese/CHIN-Chinese', "CHIN", "Chinese"],
['http://dartmouth.smartcatalogiq.com/en/2013/orc/Departments-Programs-Undergraduate/Asian-and-Middle-Eastern-Languages-and-Literatures-Arabic-Chinese-Hebrew-Japanese/HEBR-Hebrew', "HEBR", "Hebrew"],
['http://dartmouth.smartcatalogiq.com/en/2013/orc/Departments-Programs-Undergraduate/Asian-and-Middle-Eastern-Languages-and-Literatures-Arabic-Chinese-Hebrew-Japanese/JAPN-Japanese', "JAPN", "Japanese"], 
['http://dartmouth.smartcatalogiq.com/en/2013/orc/Departments-Programs-Undergraduate/The-Nelson-A-Rockefeller-Center-for-Public-Policy/Public-Policy-Minor/PBPL-Public-Policy', 'PBPL', 'Public Policy'],
['http://dartmouth.smartcatalogiq.com/en/2013/orc/Departments-Programs-Undergraduate/Institute-for-Writing-and-Rhetoric/WRIT-Writing', 'WRIT', 'Writing'], 
['http://dartmouth.smartcatalogiq.com/en/2013/orc/Departments-Programs-Undergraduate/Institute-for-Writing-and-Rhetoric/SPEE-Speech', 'SPEE', 'Speech'],
['http://dartmouth.smartcatalogiq.com/en/2013/orc/Departments-Programs-Undergraduate/Humanities/HUM-Humanities', 'HUM', "Humanities"],
['http://dartmouth.smartcatalogiq.com/en/2013/orc/Departments-Programs-Undergraduate/Physics-and-Astronomy/PHYS-Physics-Undergraduate', 'PHYS', "Physics"],
['http://dartmouth.smartcatalogiq.com/en/2013/orc/Departments-Programs-Undergraduate/Linguistics-and-Cognitive-Science/COGS-Cognitive-Science', 'COGS', "Cognitive Science"],
['http://dartmouth.smartcatalogiq.com/en/2013/orc/Departments-Programs-Graduate/Microbiology-and-Immunology/MICR-Microbiology-and-Immunology', 'MICR', 'Microbiology and Immunology']
]

# Return the section of the base url with the links to the departments
def get_link_rightpanel(url):
	r = requests.get(url)
	orig_soup = BeautifulSoup(r.content, from_encoding=r.encoding)
	return orig_soup.find("div", id='rightpanel')

# Return the links to each department's course listings
def get_course_links(url_ext, department_list):
	links = []
	for link in department_list.find_all(href=re.compile(url_ext)):
		links.append(link)
		print link

	return links

# Store the course information into the database
def store_course_info(url, course_number, course_name, dept_abbr, dept_name, year, lock_term_start, lock_term_end):

	# Convert the page to BeautifulSoup
	r = requests.get(url)
	info_soup = BeautifulSoup(r.content.decode("utf-8"), "lxml")
	
	# Search the main section of the page
	info_soup = info_soup.find( 'div', {"id" : "rightpanel"})
	if (info_soup):
		info_soup = info_soup.find('div', {'id': 'main'})
		
		if (info_soup):
			# scripts can be executed from comments in some cases  
			comments = info_soup.findAll(text=lambda text:isinstance(text, Comment))  
			for comment in comments:  
		   		comment.extract()  

	if info_soup is not None:

		# # Initialize Distribs
		# course_distributives = []
		# course_wc = None

		# # Search distributive section of listing
		# distrib_info = info_soup.find('div', {'id' : "distribution"})
		# if distrib_info is not None:

		# 	distrib_info = distrib_info.text[12:]
		# 	dists = distrib_info.split(" ")

		# 	# Check if distrib or WC for each word in section
		# 	for dist in dists:
		# 		stripped_dist = re.sub('^[^a-zA-z]*|[^a-zA-Z]*$','',dist)
				
		# 		# Add to offering if distrib
		# 		possible_distrib = Distrib.query.filter_by(distributive = stripped_dist).first()
		# 		if possible_distrib:
		# 			course_distributives.append(possible_distrib)
		# 			continue

		# 		# Add to offering if WC
		# 		possible_wc = Wc.query.filter_by(wc = stripped_dist).first()
		# 		if possible_wc:
		# 			course_wc = possible_wc

		# Check for department in database
		d1 = Department.query.filter_by(abbr = dept_abbr).first()
		if (d1 is None):
			
			# Remove Undergrad/Grad distinctions in depts
			if "Undergraduate" in dept_name:
				dept_name = dept_name.strip("Undergraduate")
			if "Graduate" in dept_name:
				dept_name = dept_name.strip("Graduate")

			print dept_name

			d1 = Department(name = dept_name, abbr = dept_abbr)
			db.session.add(d1)
			db.session.commit()

		# Check if course already exists. Add if not.
		c1 = Course.query.filter_by(number = course_number, name = course_name, department = d1).first()
		if (c1 is None):

			c1 = Course(number = course_number, name = course_name, department = d1.id)

			db.session.add(c1)
			db.session.commit()

		# Add offerings to course
		offering_info = info_soup.find('div', {'id' : "offered"})
		if offering_info is None:
			
			# If no section for offerings on page, check if it's a topics
			# course with numerous sections. 
			scan_topics_offerings(info_soup, c1, d1, year, lock_term_start, lock_term_end)

		else:
			offering_info = offering_info.text[7:]
			offerings = offering_info.split(" ")

			store_offerings(offerings, c1, d1, info_soup, year, info_soup.prettify(), lock_term_start, lock_term_end)


# Seach through the course page for each listing on the department's course listing page
def search_courses(url, dept_abbr, dept_name, year, lock_term_start, lock_term_end):

	# Convert page to BeautifulSoup
	r = requests.get(url)
	listing_soup = BeautifulSoup(r.content, from_encoding=r.encoding)

	# Find the section of the page with course listings 
	course_list = listing_soup.find( 'ul', { "class" : 'sc-child-item-links' } )
	print dept_abbr + ' - ' + dept_name
	
	# Loop through course links
	for course in course_list.find_all('a'):
		
		# Split link into name and number components
		course_to_ascii = course.text.replace(u'\xa0', u' ')
		course_split = course_to_ascii.split(' ')
		course_number = course_split[1]
		course_name = course_split[2:]

		# Fix leading space
		if course_number == '':
			course_number = course_split[2]
			course_name = course_split[3:]

		print "Department: " + dept_name
		print "Number: " + course_number
		print "Name: " + " ".join(course_name).decode("utf-8", errors='replace')

		# Store the course in the database 
		store_course_info(BASE_URL + course['href'], course_number, " ".join(course_name), dept_abbr, dept_name, year, lock_term_start, lock_term_end)

# Search through the courses in each department's listing
def search_course_links (url_ext, links, year, lock_term_start, lock_term_end):
	
	for link in links:

		right_panel = get_link_rightpanel(BASE_URL + link['href'])
		link = right_panel.find("a")
		if (link != None and url_ext in link['href']):
			link_breakdown = link['href'].split('/')
			last_link = link_breakdown[-1].split('-')
			if ('Requirements' not in last_link[-1] 
				and 'Policy' not in last_link[-1] 
				and not is_number(last_link[-1]) 
				and 'Course' not in last_link[-2] 
				and 'Major' not in last_link[-2] 
				and 'Neuroscience' not in last_link[-1]):

				search_courses(BASE_URL + link['href'], last_link[0], " ".join(last_link[1:]), year, lock_term_start, lock_term_end)

# Main function for scraping the current ORC
def scrape_college_orc(url_ext, lock_term_start, lock_term_end, start_dept_name = ""):
	
	# Use CSS formatting to find each department's link
	department_list = get_link_rightpanel(BASE_URL + url_ext)

	# Store the year of the current ORC
	year = url_ext.split("/")[2]

	# Store links to each department's course lists
	links = get_course_links(url_ext, department_list)

	# If debugging the scraping, find debugger's starting department
	abbr_index = find_starting_abbr(links, start_dept_name)

	# Search through the courses in each department
	search_course_links (url_ext, links[abbr_index:], int(year), lock_term_start, lock_term_end)

	return int(year)

	

def scrape_curr_orc(lock_term_start, lock_term_end, start_dept_name = ""):
	scrape_college_orc(UG_DEPT_URL, lock_term_start, lock_term_end, start_dept_name = "")
	year = scrape_college_orc(GRAD_DEPT_URL, lock_term_start, lock_term_end, start_dept_name = "")

	# Repeat for all missed departments
	for listing in MISSED_UG_LISTINGS:
		search_courses(listing[0], listing[1], listing[2], year, lock_term_start, lock_term_end)
