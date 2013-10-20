import os

from bs4 import BeautifulSoup, BeautifulStoneSoup
import unicodedata
import requests
import re

from app import db
from app.models import User, Offering, Course, Department, Hour, Distrib, Wc, Term

# Base URLs
BASE_URL = "http://dartmouth.smartcatalogiq.com"
UG_DEPT_URL = "/en/2013/orc/Departments-Programs-Undergraduate"

# List of all departments missed in scraping of the ORL
# Format: URLs, Abbreviation, Name
MISSED_LISTINGS = [['http://dartmouth.smartcatalogiq.com/en/2013/orc/Departments-Programs-Undergraduate/Classics-Classical-Studies-Greek-Latin/LAT-Latin', 'LAT', 'Latin'], 
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
['http://dartmouth.smartcatalogiq.com/en/2013/orc/Departments-Programs-Undergraduate/Physics-and-Astronomy/PHYS-Physics-Undergraduate', 'PHYS', "Physics"]]

# Distributives and World Culture Abbreviations
DISTRIBS = ["ART", "LIT", "TMV", "INT", "SOC", "QDS", "SCI", "SLA", "TAS", "TLA"]
WCS = ["W", "NW", "CI"]

# Hours and Seasons
HOURS = ["8", "9", "9L", "9S", "10", "10A", "11", "12", "2", "2A", "3A", "3B", "Arrange", "8AM-9:50AM", "3-6pm", "7pm", "2:00-4:00", "2:00-6:00", "2:00-3:05pm", "8-10", "4-6pm", "4-6PM", "T3-6", "3-6", "D.F.S.P", "D.L.S.A", "FSP", "2-5pm", "1:00-3:00", "4:00-5:00", "4:00-6:00", "6-9", "3:00-5:00", "2-5", "1"]
SEASONS = ["W", "S", "X", "F"]

# Alert function that makes a message stand out when running hte scraper
def print_alert(message):
	print ('\n\n')
	print '*******' + message + '*******\n'

# Helper to check if string is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Add all missing distribs and World Cultures to the database
def store_distribs():
	for distrib in DISTRIBS:
		dist1 = Distrib.query.filter_by(distributive = distrib).first()
		if (dist1 is None):
			dist1 = Distrib(abbr = distrib)
			db.session.add(dist1)
			db.session.commit()

	for wc in WCS:
		wc1 = Wc.query.filter_by(wc = wc).first()
		if (wc1 is None):
			wc1 = Wc(abbr = wc)
			db.session.add(wc1)
			db.session.commit()

# Add all missing hours to the database
def store_hours():
	for hour in HOURS:
		hour1 = Hour.query.filter_by(period = hour).first()
		if (hour1 is None):
			hour1 = Hour(period = hour)
			db.session.add(hour1)
			db.session.commit()

# Add all missing terms to the database
def store_terms():
	for year in range(2005, 2099):
		for season in SEASONS:
			t = Term.query.filter_by(year=year, season=season).first()
			if t is None:
				t = Term(year, season)
				db.session.add(t)

	db.session.commit()

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
def store_offerings(offering_info, c1, d1, info_soup, year):
	# Initialize offered lists to empty
	terms_offered = []
	hours_offered = []

	# Initialize first category to TERM
	new_category = "TERM"
	old_category = ""

	# Loop each word in the offering listing
	for offer in offering_info:
		
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

		# Ignore Lab and Discussion hours 
		if "LAB" in stripped_offering.upper():
			break
		if "DISCUSSION" in stripped_offering.upper():
			break

		# Assume this might lead to "Times vary", so continue
		if "Times" in stripped_offering:
			continue

		# If "Dist:" in offering listing, skip
		if "Dist" in stripped_offering:
			break

		# If offerings vary, should check for topics offerings
		if stripped_offering == "Varies" or stripped_offering == "vary:
			scan_topics_offerings(info_soup, c1, d1, year)
			break

		# Check for other key terms that signal a halt in offerings
		if stripped_offering == "See":
			break
		if "Section" in stripped_offering:
			break
		if "field" in stripped_offering:
			break
		if "Field" in stripped_offering:
			break

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
		stripped_offering = fix_offering_typos(c1, d1, stripped_offering, hours_offered, terms_offered, old_category, new_category)

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

# Generalized check for missing space between terms and hours
def check_misplaced_colon(stripped_offering, hours_offered, terms_offered, old_category, new_category):
	
	if (":" in stripped_offering):
		if terms_offered != []:
			return stripped_offering

		# Store first half of colon as year
		split_colon = stripped_offering.split(":")
		year = "20" + split_colon[0][:2]
		season = split_colon[0][2]

		# Add the term to terms_offered
		possible_term = Term.query.filter_by(year = int(year), season = str(season)).first()
		if possible_term:
			terms_offered.append(possible_term)
			old_category = new_category
			new_category = "TERM"

		# Return to previous function with second half (hour) as 
		# stripped_offering
		stripped_offering = split_colon[1]

	return stripped_offering

# Generalized check for missing space between either terms or hours
def check_misplaced_comma(stripped_offering, hours_offered, terms_offered):
	if ("," in stripped_offering):

		split_comma = stripped_offering.split(",")

		# Check whether term or hour for each component in the unintentionally 
		# un-spaced list
		for i in range(len(split_comma) - 1):
			
			# Check if possible hour, and if so, add to the hours offered
			possible_hour = Hour.query.filter_by(period = split_comma[i]).first()
			if possible_hour:
				hours_offered.append(possible_hour)
				continue
			
			# If not hour, assume term and add to terms offered
			year = "20" + split_comma[i][:2]
			season = split_comma[i][2]
			possible_term = Term.query.filter_by(year = year, season = season).first()
			if possible_term:
				terms_offered.append(possible_term)
				continue
		
		# Return to previous function with last component as stripped_offering
		stripped_offering = split_comma[len(split_comma) - 1]

	return stripped_offering

# Helper to append all terms covered by an ORC to the terms_offered list
def add_all_terms(year, terms_offered):
	
	# Store all possible years
	fall_year = year
	years = [year + 1, year + 2]
	
	# Add fall of that year to offerings
	possible_term = Term.query.filter_by(year = fall_year, season = "F").first()
	if (possible_term):
		terms_offered.append(possible_term)

	# Add every term of the other two years covered by the ORC
	for year_after in years:
		for season in SEASONS:
			possible_term = Term.query.filter_by(year = year_after, season = season).first()
			if (possible_term):
				terms_offered.append(possible_term)

def remove_all_summer_terms(year, terms_offered):
	years = [year + 1, year + 2]
	for year_after in years:
		for summer_term in Term.query.filter_by(year = year_after, season = "X").all():
			terms_offered.remove(summer_term)

# When debugging, find index in links of desired starting department
def find_starting_abbr(links, start=""):

	abbr_index = 0

	print start

	if (start != ""):
		for s in links:
			print s
			if start in s:
				abbr_index = links.index(s)
				break

	return abbr_index

# Mark all remaining courses as empty again
def remove_course_marks():
	all_courses = Offering.query.all()
	for course in all_courses:
		course.mark_empty()

	db.session.commit()

# Delete all terms not marked as added, because they were not found in the 
# latest scraping. Then reset all "added" flags for next scraping.
def remove_deleted_offerings():
	deleted_courses = Offering.query.filter_by(added = "").all()

	for course in deleted_courses:
		db.session.delete(course)

	db.session.commit()

	remove_course_marks()

# Add all possible combinations of terms and hours to course's offerings 
def add_offerings(course, terms_offered, hours_offered):
	print terms_offered
	print hours_offered
	print "\n"

	# Loop through all combinations
	for term in terms_offered:
		for hour in hours_offered:

			# Check if offering already exists
			o1 = Offering.query.filter_by(course_id = course.id, term_id = term.id, hour_id = hour.id).first()
			
			# Add offering if not already in database
			if o1 is None:
				o1 = Offering(course = course.id, term = term.id, hour = hour.id)
				db.session.add(o1)		
				
				print_alert(str(o1))
			
			# Mark offering as added to check for deleted offerings at end
			o1.mark_added()

	db.session.commit()

	# Clear offering tables and restarted flag checking
	return [], [], "TERM"