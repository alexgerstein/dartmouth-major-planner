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

# Check each stripped offering for typos in the ORC's listing
def fix_offering_typos(c1, d1, stripped_offering, hours_offered, terms_offered, old_category, new_category):
	
	# "Asian and Middle Eastern Languages": Different formatting of language courses
	if (d1.abbr == "AMEL"):
		if (len(stripped_offering) < 3) and (terms_offered == []):
			c1 = Course.query.filter_by(department = d1, number = stripped_offering).first()
			stripped_offering = ""
		elif (stripped_offering[len(stripped_offering) - 1] == ','):
			c1 = Course.query.filter_by(department = d1, number = stripped_offering[:2]).first()
			stripped_offering = ""
	
	# "Chemistry": Different formatting of CHEM 5 and others
	if (d1.abbr == "CHEM"):
		if (len(stripped_offering) < 3 and (terms_offered == [])):
			c1 = Course.query.filter_by(department = d1, number = stripped_offering).first()
			stripped_offering = ""

	# "Classics": Intermediate Latin missing space between hours offered
	if (d1.abbr == "CLST"):
		if (c1.name == "Intermediate Latin"):
			if (stripped_offering == "9,2"):
				possible_hour = Hour.query.filter_by(period = "9").first()
				hours_offered.append(possible_hour)
				stripped_offering = "2"

	# "Earth Sciences": Invalid initial character for some years
	if (d1.abbr == "EARS"):
		if (c1.number == "70"):
			stripped_offering = ""

	# "Government": Misplaced colon
	if (d1.abbr == "GOVT"):
		if 60 == c1.number:
			if "11:F" in stripped_offering:
				stripped_offering = "11F"

	# "International Studies": Missing space between term and hour
	if (d1.abbr == "INTS"):
		if stripped_offering == "12W:W":
			possible_term = Term.query.filter_by(year = "2012", season = "W").first()
			terms_offered.append(possible_term)
			stripped_offering = ""

	# "Mathematics": Some courses are no longer offered
	if (d1.abbr == "MATH"):
		if (c1.name == "Discrete Mathematics in Computer Science"):
			stripped_offering = ""
		elif "Linear Programming" in c1.name:
			stripped_offering = ""

	# "Music": Individual music have section numbers that get confused as hours
	if (d1.abbr == "MUS"):
		if (c1.name == "Performance Laboratories"):
			if len(stripped_offering) == 1:
				stripped_offering = ""

	stripped_offering = check_misplaced_colon(stripped_offering, hours_offered, terms_offered, old_category, new_category)

	stripped_offering = check_misplaced_comma(stripped_offering, hours_offered,terms_offered)

	return stripped_offering

# Loop through each offering, adding the terms to a list of offered terms and 
# the hours to a list of offered hours. When the category of the offerings 
# switch from terms offered to hours offered and back, we know that all 
# possible combinations have been found. So we run these combinations through 
# the add_offerings function.
#
# For example, an offerings list is often in the format: 
# 	"[TERM1], [TERM2]: [HOUR1], [HOUR2]"
# In this case, there would be 4 offerings, one for each combination of the
# terms and hours
def store_offerings(offerings, c1, dept, year):
	# Initialize offered lists to empty
	terms_offered = []
	hours_offered = []

	# Initialize first category to TERM
	new_category = "TERM"
	old_category = ""

	# Loop each word in the offering listing
	for offer in offerings:
		
		# Remove any non-alphanumeric characters on each end
		stripped_offering = re.sub('(^[\W_]*)|([\W_]*$)', '', offer)
		print stripped_offering

		# Move to next component if blank
		if stripped_offering == "":
			continue

		# If first word is "Not", then assume it continues "Not offered..." 
		# and break
		if stripped_offering == "Not":
			break

		# Ignore Lab and Discussion hours 
		if "LAB" in stripped_offering.upper():
			break
		if "DISCUSSION" in stripped_offering.upper():
			break

		# If "Dist:" in offering listing, skip
		if "Dist" in stripped_offering:
			break

		# If offering starts with "All," assume that it continues "All Terms."
		# Then add All Terms in the current ORC using the year from the url
		if stripped_offering == "All":
			add_all_terms(year, terms_offered)

			# Switch categories to mark TERM as just having been checked
			old_category = new_category
			new_category = "TERM"
			continue

		# If "summer" is in the listing, then assume it reads "All terms, 
		# except summer." So, remove all summer terms in the list of terms
		# offered.
		if stripped_offering == "summer":
			remove_all_summer_terms(year, terms_offered)
			
			# Switch categories to mark TERM as just having been checked
			old_category = new_category
			new_category = "TERM"
			continue

		# Since the "period" Arrange is not a number, check for it early and
		# add it to the list of possible hours before issues arise.
		if stripped_offering == "Arrange":
			possible_hour = Hour.query.filter_by(period = "Arrange").first()
			if possible_hour:
				hours_offered.append(possible_hour)
				old_category = new_category
				new_category = "HOUR"

			# Assume no other hours offered, since Arrange is usually listed 
			# for the later terms, so run combinator fcn for offering lists 
			terms_offered, hours_offered, new_category = add_offerings(c1, terms_offered, hours_offered)
			continue

		# Similar to "Arrange", these FSP periods are not numbers, so check and
		# add them early.
		if stripped_offering == "FSP" \
		or stripped_offering == "D.F.S.P" \
		or stripped_offering == "D.L.S.A":
			possible_hour = Hour.query.filter_by(period = stripped_offering).first()
			if (possible_hour):
				hours_offered.append(possible_hour)
				old_category = new_category
				new_category = "HOUR"

		# If first digit of the offering is not a number, then it can no 
		# longer be a term or a period
		if not is_number(stripped_offering[0]):
			continue

		# Check for typos on the ORC listing
		stripped_offering = fix_offering_typos(c1, dept, stripped_offering, hours_offered, terms_offered, old_category, new_category)

		# If typo check returned nothing, then add the current combinations
		# to the offerings and move on to the next word in offerings
		if stripped_offering == "":
			terms_offered, hours_offered, new_category = add_offerings(c1, terms_offered, hours_offered)
			continue

		# Check if word is an hour. If it is, append it to hours_offered
		possible_hour = Hour.query.filter_by(period = stripped_offering).first()
		if possible_hour:
			hours_offered.append(possible_hour)
			old_category = new_category
			new_category = "HOUR"

			continue

		# Check if word is a term. If it is, append it to terms_offered
		possible_term = Term.query.filter_by(year = int("20" + stripped_offering[:2]), season = stripped_offering[2]).first()
		if possible_term:
			old_category = new_category
			new_category = "TERM"

			# If the categories swapped from hours, back to term, then add all
			# possible combinations of the terms and hours
			if (old_category != "" and old_category != new_category):
				terms_offered, hours_offered, new_category = add_offerings(c1, terms_offered, hours_offered)

			# Append the new term
			terms_offered.append(possible_term)

	# Now that loop has been exited, add then clear any remaining combinations
	terms_offered, hours_offered, new_category = add_offerings(c1, terms_offered, hours_offered)

# Use the "coursetitle" class to find each course in the department's listing
def add_offerings_by_tag(soup, dept, year):

	# For each course in the listing, add offerings to the database
	for title in soup.find_all("p", { "class" : "coursetitle" }):
		
		# Split the course heading into its number and name
		split_title = title.text.strip(" ").split(" ")
		course_number = split_title[0].strip(".")
		course_name = " ".join(split_title[1:]).strip(" ")

		print "Number: " + str(course_number)
		print "Name: " + course_name
		print "Dept: " + str(dept)

		# Look for the course in the database by department
		course = Course.query.filter_by(number = str(course_number), department_id = dept.id).first()
		if not (is_number(course_number[0])) and (course is None):
			break

		# If course not in database, add it.
		if (course is None):
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

		# For each list of offerings of the course, add to the database
		while (offerings['class'] ==  ["courseoffered"]):
			
			# Split the offering into a list of each word
			offering_split = offerings.text.split(" ")

			# Iterate through the list of words, storing each offering
			store_offerings(offering_split, c1, dept, year)

			# Step to next set of offerings
			offerings = offerings.findNext("p")

			if not "class" in offerings:
				break

	return

# If page is formatted differently than the latest archived ORCs, do nothing with them
def add_offerings_by_headers(soup, dept):
	return

# Scrape a department's courses and offerings off its "Courses" page
def get_old_courses(url, dept):
	
	# Convert page to BeautifulSoup
	r = requests.get(url)
	soup = BeautifulSoup(r.content.decode("utf-8"))

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
		add_offerings_by_tag(soup, d1, int(year))
	else:
		add_offerings_by_headers(soup, d1)

# Main function for scraping the archived ORCs 
def scrape_old_orcs(start_abbr = ""):
	
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

			get_old_courses(course_link, dept_abbr)
