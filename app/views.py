# views.py
# Alex Gerstein
# Routes for the user

from flask import render_template, request, flash, redirect, url_for, session, g, jsonify
from app import app, db
from models import User, Offering, Course, Department, Term, Hour
from forms import EditForm, DeptPickerForm, HourPickerForm, TermPickerForm
from functools import wraps

SEASONS = ["W", "S", "X", "F"]

# Wrapper function so certain pages remain private to new users
def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('flask_cas.login'))

        return fn(*args, **kwargs)
    return wrapper

# Wrapper to make sure students can't view planner without giving it its range
def year_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        if g.user.grad_year is None:
            return redirect(url_for('edit'))

    	return fn(*args, **kwargs)
    return wrapper

def generate_terms(grad_year):
	all_terms = []

	# Add Freshman Fall
	t = Term.query.filter_by(year=grad_year - 4, season=SEASONS[3]).first()
	if t is None:
		t = Term(grad_year - 4, SEASONS[3])
		db.session.add(t)

	all_terms.append(t)

	for year_diff in reversed(range(4)):
		for season in SEASONS:
			t = Term.query.filter_by(year=grad_year - year_diff, season=season).first()
			if t is None:
				t = Term(grad_year - year_diff, season)
				db.session.add(t)
			
			all_terms.append(t)

	# Remove extra fall
	all_terms.remove(t)

	return all_terms

# If graduation year changes for user, adjusts terms in planner
def add_terms(terms):
	
	# Clear all terms, start clean
	for term in g.user.terms:
		g.user.remove_term(term)
		db.session.commit()

	for term in terms:
		g.user.add_term(term)
		db.session.commit()

# Helper method to get the offering a user is editing on the planner interface
def get_requested_offering(form):
	
	# Deconstruct the dragged item's id to get the course from the database
	split_course = request.form["course"].strip().split(" ")
	d1 = Department.query.filter_by(abbr = split_course[0]).first()
	c1 = Course.query.filter_by(number = split_course[1], department = d1).first()
	
	# Construct the requested offering based on where dropped
	year = "20" + request.form['term'][:2]
	season = request.form['term'][2]
	t = Term.query.filter_by(year = year, season = season).first()

	# Construct the requested hour if one exists
	if 'hour' not in request.form:
		offering = Offering.query.filter_by(course = c1, term = t).first()

		if offering is None:
			hour = Hour.query.filter_by(period = "?").first()
		else:
			hour = offering.get_hour() 
	else:
		hour_string = request.form['hour']
		hour = Hour.query.filter_by(period = hour_string).first()

	o1 = Offering.query.filter_by(course = c1, term = t, hour = hour).first()
	if o1 is None:

		check_hour = Hour.query.filter_by(period = "?").first()

		o1 = Offering(course = c1.id, term = t.id, hour = check_hour.id, desc = "***User Added***<br>Consult registrar for more info", user_added = "Y")
		db.session.add(o1)

		db.session.commit()

	return o1


# Always track if there is a current user signed in
# If unrecognized user is in, add them to user database
@app.before_request
def fetch_user():

	if 'user' in session:
		g.user = User.query.filter_by(netid=session['user']['netid']).first()
		if g.user is None:
			g.user = User(session['user']['name'], session['user']['netid'])
			db.session.add(g.user)
			db.session.commit()
			return (redirect(url_for('edit')))
	else:
		g.user = None

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html",
        title = 'Home',
        user_count = User.query.count())

# Planner page for signed in users
# Landing Page for All Users, most will be redirected to login form
@app.route('/planner', methods = ['GET'])
@login_required
@year_required
def planner():

	# Initialize the department selection form
	dept_form = DeptPickerForm()
	dept_form.dept_name.choices = [(a.id, a.abbr + " - " + a.name) for a in Department.query.order_by('abbr')]
	dept_form.dept_name.choices.insert(0, (-1,"Choose a Department"))

	# Initialize the hour selection form
	hour_form = HourPickerForm()
	hour_form.hour_name.choices = [(a.id, a.period) for a in Hour.query.order_by('id')]
	hour_form.hour_name.choices.insert(0, (-1,"Choose an Hour"))

	# Initialize the term selection form
	term_form = TermPickerForm()
	term_form.term_name.choices = [(a.id, str(a)) for a in g.user.terms.order_by('year', 'id')]
	term_form.term_name.choices.insert(0, (-1,"Choose a Term"))

	all_terms = generate_terms(g.user.grad_year)

	# Check if terms aren't in the session
	if g.user.terms is None:
		add_terms(all_terms)
		db.session.commit()

	return render_template("planner.html",
        title = 'My Plan',
        user = g.user,
        dept_form = dept_form,
        hour_form = hour_form,
        term_form = term_form,
        courses = g.user.courses.order_by('hour_id'),
        on_terms = g.user.terms.order_by('year', 'id'),
        terms = all_terms)

# After change in dept form, send courses in that dept to user's view
@app.route('/getcourses', methods = ['POST'])
@login_required
def getcourses():

	courses = None
	if request.form['dept'] != "-1":
		courses = Course.query.filter_by(department_id = request.form['dept']).join(Offering)
	elif request.form['term'] != "-1" or request.form['hour'] != "-1":
		courses = Course.query

	if request.form['term'] != "-1":
		courses = courses.filter_by(term_id = request.form['term'])

	if request.form['hour'] != "-1":
		courses = courses.filter_by(hour_id = request.form['hour'])

	if courses is None:
		j = jsonify ( {} )
	else:
		j = jsonify( { 'courses' : [i.serialize for i in courses.order_by('number')] })

	return j

# If new course dragged into a box, store it in the user's courses
# Send the hour of the offering to the user
@app.route('/savecourse', methods = ['POST'])
@login_required
def savecourse():

	offering = get_requested_offering(request.form)

	success = None
	if offering is not None:
		success = g.user.take(offering)

	if success is None:
		j = jsonify( { 'error' : "Course could not be added" } )
		return j

	j = jsonify( { 'name' : str(offering), 'hour' : str(offering.get_hour()), 'possible_hours' : offering.get_possible_hours() } )

	return j

# If user selects new hour from dropdown, update database.
@app.route('/swaphour', methods = ['POST'])
@login_required
def swaphour():
	
	offering = get_requested_offering(request.form)

	hour = Hour.query.filter_by(period = request.form['new_hour']).first()
	success = False
	if offering is not None:
		success = g.user.switch_hour(offering, hour)

	if not success:
		j = jsonify( { 'error' : "Course could not be swapped" } )
		return j

	j = jsonify( { 'name' : str(offering), 'hour' : str(hour), 'possible_hours' : offering.get_possible_hours() } )

	return j

# Callback to delete a course if user pressed red "Trash" button
@app.route('/removecourse', methods = ['POST'])
@login_required
def removecourse():
	
	offering = get_requested_offering(request.form)
	
	success = None
	if offering is not None:
		success = g.user.drop(offering)

	if not success:
		j = jsonify( { 'error' : "Course could not be dropped" } )
		return j


	j = jsonify ( { 'error' : "", 'course' : str(offering) })

	return j

# Callback to see text of course offering
@app.route('/getCourseInfo', methods = ['POST'])
@login_required
def getCourseInfo():

	offering = get_requested_offering(request.form)

	return jsonify ( { "info" : offering.desc})

# Callback to send all available terms of course so they can be highlighted on planner
@app.route('/findterms', methods = ['POST'])
@login_required
def findterms():
	
	# Get Course
	split_course = request.form['course'].strip().split(" ")
	d1 = Department.query.filter_by(abbr = split_course[0]).first()
	c1 = Course.query.filter_by(number = split_course[1], department = d1).first()

	available_user_offerings = Offering.query.filter_by(course = c1, user_added = "Y").all()
	available_registrar_offerings = Offering.query.filter_by(course = c1, user_added = "N").all()

	# Send array of terms to client's view
	j = jsonify( { 'terms' : [str(i.term) for i in available_registrar_offerings], 'user-terms': [str(i.term) for i in available_user_offerings] })

	return j

# Toggle on/off terms
@app.route('/swapterm', methods = ['POST'])
@login_required
def swapterm():
	
	# Get term from database
	term_name = request.form['term']
	year = "20" + request.form['term'][:2]
	season = request.form['term'][2]
	t1 = Term.query.filter_by(year = year, season = season).first()

	g.user.swap_onterm(t1)
	db.session.add(g.user)
	db.session.commit()

	j = jsonify( {} )

	return j

# Settings redirect's to user's own profile page
# TODO: Have profile show current plan
@app.route('/settings')
@login_required
def settings():
	return render_template('user.html', title = 'Settings', 
		user = g.user)

# Edit Page to change Name and Graduation Year
@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
	form = EditForm(g.user.nickname)
	
	if form.validate_on_submit():
		g.user.nickname = form.nickname.data
		g.user.grad_year = form.grad_year.data

		add_terms(generate_terms(form.grad_year.data))
		db.session.commit()


		return redirect(url_for('planner'))
	else:
		# Reset form to current entries
		form.nickname.data = g.user.nickname
		form.grad_year.data = g.user.grad_year
	return render_template('edit.html',
		form = form, title = 'Settings', user = g.user)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):

    return render_template('500.html'), 500