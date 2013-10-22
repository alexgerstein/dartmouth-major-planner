# scrape_old_orcs.py
# Alex Gerstein

from scrape_functions import *

# Base URL for achived ORCs
PAST_BASE_URL = "http://www.dartmouth.edu/~regarchive"

# Return the section of the base url with the links to the archived ORCs
def get_old_links(base_url):
	r = requests.get(base_url)
	orig_soup = BeautifulSoup(r.content, from_encoding=r.encoding)
	return orig_soup.find("div", style='float:left; margin-right:30px; width:40%')

# Return the links to each year's archived ORC
def get_old_course_links(course_year_list):
	links = []
	for year_link in course_year_list.find_all('a'):
		links.append(year_link['href'])

	return links

# Adjust any URL typos to match the departments in our database
def fix_dept_typos(dept):
	if dept == "INST":
		dept = "INTS"
	if dept == "M-SS":
		dept = "MSS"

	return dept

# Use the "coursetitle" class to find each course in the department's listing
def add_offerings_by_tag(soup, dept, year, lock_term_start, lock_term_end):

	# For each course in the listing, add offerings to the database
	for title in soup.find_all("p", { "class" : "coursetitle" }):

		# Split the course heading into its number and name
		split_title = title.text.strip(" ").split(" ")
		course_number = split_title[0].strip(".")
		course_name = " ".join(split_title[1:]).strip(" ")

		abbreviation = dept.abbr

		old_dept = dept

		# Adjust for AMEL department
		if old_dept.abbr == "AMEL":
			if "Arab" in course_name:
				abbreviation = "ARAB"
			elif "Chinese" in course_name:
				abbreviation = "CHIN"
			elif "Hebrew" in course_name:
				abbreviation = "HEBR"
			elif "Japanese"in course_name:
				abbreviation = "JAPN"

			dept = Department.query.filter_by(abbr = abbreviation).first()

		print "Number: " + str(course_number)
		print "Name: " + course_name
		print "Dept: " + str(dept)

		# Look for the course in the database by department
		course = Course.query.filter_by(number = str(course_number), department_id = dept.id).first()
		if not (is_number(course_number[0])) and (course is None):
			dept = old_dept
			continue

		# If course not in database, add it.
		if (course is None) and len(name) < 300:
			course = Course(number = course_number, name = course_name, department = dept.id)
			db.session.add(course)
			db.session.commit()

		# Store the next section (usually the offerings)
		offerings = title.findNext("p")

		# If no next section, or next section is not a course, stop scraping the page
		if offerings is None:
			break
		if (offerings.text == "Contact Us"):
			break

		# Initialize concatenated offering description for info page
		offering_html = title

		# For each list of offerings of the course, add to the database
		while (offerings['class'] ==  ["courseoffered"]):
			
			# Split the offering into a list of each word
			offering_split = offerings.text.split(" ")

			print course

			# Concatenate listing from orc page
			offering_html.append(offerings)
			description = offerings.findNext('p', {'class': 'coursedescptnpar'})
			while (description is not None) and (description['class'] == ['coursedescptnpar']):
				
				# Append description and look for another
				offering_html.append(description)
				description = description.findNext("p")

				# Check if tag was incorrectly assigned to title
				if (description is not None) and (description.get("class") == ['coursetitle']):
					if not is_number(description.text[0]):
						description = description.findNext("p")

				if description and description.get("class"):
					continue
				else:
					break

			# Iterate through the list of words, storing each offering
			store_offerings(offering_split, course, dept, soup, year, offering_html, lock_term_start, lock_term_end)

			# Step to next set of offerings
			offerings = offerings.findNext("p")

			# Reset info page html
			offering_html = title

			if 'class' in offerings:
				continue
			else:
				break

		dept = old_dept

	return

# If page is formatted differently than the latest archived ORCs, do nothing with them
def add_offerings_by_headers(soup, dept):
	return

# Scrape a department's courses and offerings off its "Courses" page
def get_old_courses(url, dept, lock_term_start, lock_term_end):
	
	# Convert page to BeautifulSoup
	r = requests.get(url)
	soup = BeautifulSoup(r.content.decode("utf-8"), "lxml")

	# Parse out the year from the curret url
	split_url = url.split("/")
	year_with_desc = split_url[len(split_url) - 2]
	year = year_with_desc.strip("desc")

	# Fix any typos in the URL to store the department abbreviation
	dept = fix_dept_typos(dept)

	# Look up the department in the database. Return if it does not exist
	d1 = Department.query.filter_by(abbr = dept).first()
	if (d1 is None):
		print_alert("MISSING DEPT " + dept)
		return

	# Depending on how the page is formatted, call the appropriate function to scrape the page
	if soup.find("p", { "class" : "coursetitle" } ):
		add_offerings_by_tag(soup, d1, int(year), lock_term_start, lock_term_end)
	else:
		add_offerings_by_headers(soup, d1)

# Main function for scraping the archived ORCs 
def scrape_old_orcs(lock_term_start, lock_term_end, start_abbr = ""):
	
	# Use CSS formatting to find each department's link
	old_orc_links = get_old_links(PAST_BASE_URL)
	links = get_old_course_links(old_orc_links)
	
	# The oldest three archived ORCs have different CSS styling than the others. Leave them be.
	for link in links[len(links) - 3:]:
		continue

	# Get and scrape each department's listings for the other ORCs
	for link in links[:len(links) - 3]:
		
		# Trim off the excess '/~regarchive' of each link
		trim_link = link[12:]

		# Convert the page to BeautifulSoup to seach by CSS
		r = requests.get(PAST_BASE_URL + trim_link)
		soup = BeautifulSoup(r.content, from_encoding=r.encoding)

		# Store links to each department's course listings
		course_links = []
		for course_link in soup.find_all('td', text="Courses"):
			new_link = course_link.find('a')['href']
			if PAST_BASE_URL not in new_link:
				new_link = PAST_BASE_URL + new_link[12:]

			course_links.append(new_link)

		# If debugging the scraping, find debugger's starting department
		shortened_index = find_starting_abbr(course_links, start_abbr)

		# For each course listings link, go to deptartment's 'Courses' page 
		# and scrape
		for course_link in course_links[shortened_index:]:		

			department = course_link.split("/")
			dept_abbr = department[len(department) - 1].split(".")[0].upper()

			get_old_courses(course_link, dept_abbr, lock_term_start, lock_term_end)
