from scrape_functions import *

# Return the section of the base url with the links to the departments
def get_link_rightpanel(url):
	r = requests.get(url)
	orig_soup = BeautifulSoup(r.content, from_encoding=r.encoding)
	return orig_soup.find("div", id='rightpanel')

# Return the links to each department's course listings
def get_undergrad_course_links(department_list):
	links = []
	for link in department_list.find_all(href=re.compile(UG_DEPT_URL)):
		links.append(link)

	return links

# Check for offerings being listed in the sections of a topics course
# For example, some descriptions start: "13F at 2..."
def scan_topics_offerings(course_soup, course, dept, year):
	text = course_soup.text

	# Regex search for all instances of "[TERM] at [HOUR]"
	for offering in course_soup.find_all(text=re.compile('[0-9][0-9][FWSX] at [0-9A-Z]{1,2}')):
		split_offering = offering.split(" ")
		store_offerings(split_offering, course, dept, course_soup, year)

# Check each stripped offering for typos in the ORC's listing
def fix_offering_typos(c1, d1, stripped_offering, hours_offered, terms_offered, old_category, new_category):

	# "Economics": Missing F for fall in term listed
	if (c1.name == "International Finance and Open-Economy Macroeconomics"):
		if (str(stripped_offering) == "14"):
			stripped_offering = "14F"

	# "Spanish LSA": Missing X for summer
	if (c1.name == "Language Study Abroad"):
		if (stripped_offering =="14"):
			if (d1.abbr == "SPAN"):
				stripped_offering = "14X"

	# "Music": Individual music have section numbers that get confused as hours
	if (c1.name == "Performance Laboratories"):
		for possible_term in Term.query.all():
			terms_offered.append(possible_term)
		possible_hour = Hour.query.filter_by(period = "Arrange").first()
		if possible_hour:
			hours_offered.append(possible_hour)

		stripped_offering = ""

	# "German": Misplaced colon
	if (c1.name == "Studies in German History"):
		if (stripped_offering == "14:F"):
			stripped_offering = "14F"

	stripped_offering = check_misplaced_colon(stripped_offering, hours_offered, terms_offered, old_category, new_category)

	stripped_offering = check_misplaced_comma(stripped_offering, hours_offered,terms_offered)

	return stripped_offering

# Store the course information into the database
def store_course_info(url, course_number, course_name, dept_abbr, dept_name, year):

	# Convert the page to BeautifulSoup
	r = requests.get(url)
	info_soup = BeautifulSoup(r.content.decode("utf-8"))
	
	# Search the main section of the page
	info_soup = info_soup.find( 'div', {"id" : "rightpanel"})
	if info_soup is not None:

		# Initialize Distribs
		course_distributives = []
		course_wc = None

		# Search distributive section of listing
		distrib_info = info_soup.find('div', {'id' : "distribution"})
		if distrib_info is not None:

			distrib_info = distrib_info.text[12:]
			dists = distrib_info.split(" ")

			# Check if distrib or WC for each word in section
			for dist in dists:
				stripped_dist = re.sub('^[^a-zA-z]*|[^a-zA-Z]*$','',dist)
				
				# Add to offering if distrib
				possible_distrib = Distrib.query.filter_by(distributive = stripped_dist).first()
				if possible_distrib:
					course_distributives.append(possible_distrib)
					continue

				# Add to offering if WC
				possible_wc = Wc.query.filter_by(wc = stripped_dist).first()
				if possible_wc:
					course_wc = possible_wc

		# Check for department in database
		d1 = Department.query.filter_by(name = dept_name).first()
		if (d1 is None):
			d1 = Department(name = dept_name, abbr = dept_abbr)
			db.session.add(d1)
			db.session.commit()

		# Check if course already exists. Add if not.
		c1 = Course.query.filter_by(number = course_number, name = course_name, department = d1).first()
		if (c1 is None):
			
			if (course_wc is None):
				wc_id = None
			else:
				wc_id = course_wc.id

			c1 = Course(number = course_number, name = course_name, department = d1.id)

			db.session.add(c1)
			db.session.commit()

		# Add offerings to course
		offering_info = info_soup.find('div', {'id' : "offered"})
		if offering_info is None:
			
			# If no section for offerings on page, check if it's a topics
			# course with numerous sections. 
			scan_topics_offerings(info_soup, c1, d1, year)

		else:
			offering_info = offering_info.text[7:]
			offerings = offering_info.split(" ")

			store_offerings(offerings, c1, d1, info_soup, year)


# Seach through the course page for each listing on the department's course listing page
def search_courses(url, dept_abbr, dept_name, year):
	
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
		print "Name: " + " ".join(course_name)

		# Store the course in the database 
		store_course_info(BASE_URL + course['href'], course_number, " ".join(course_name), dept_abbr, dept_name, year)

# Search through the courses in each department's listing
def search_course_links (links, year):
	
	for link in links:
	
		right_panel = get_link_rightpanel(BASE_URL + link['href'])
		link = right_panel.find("a")
		if (link != None and UG_DEPT_URL in link['href']):
			link_breakdown = link['href'].split('/')
			last_link = link_breakdown[-1].split('-')
			if ('Requirements' not in last_link[-1] 
				and 'Policy' not in last_link[-1] 
				and not is_number(last_link[-1]) 
				and 'Course' not in last_link[-2] 
				and 'Major' not in last_link[-2] 
				and 'Neuroscience' not in last_link[-1]):

				search_courses(BASE_URL + link['href'], last_link[0], " ".join(last_link[1:]), year)

# Main function for scraping the current ORC
def scrape_curr_orc(start_dept_name = ""):
	
	# Use CSS formatting to find each department's link
	department_list = get_link_rightpanel(BASE_URL + UG_DEPT_URL)

	# Store the year of the current ORC
	year = UG_DEPT_URL.split("/")[2]

	# Store links to each department's course lists
	links = get_undergrad_course_links(department_list)
	
	# If debugging the scraping, find debugger's starting department
	abbr_index = find_starting_abbr(links, start_dept_name)
	
	# Search through the courses in each department
	search_course_links (links[abbr_index:], int(year))

	# Repeat for all missed departments
	for listing in MISSED_LISTINGS:
		search_courses(listing[0], listing[1], listing[2], int(year))
