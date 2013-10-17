from flask import render_template, request, flash, redirect, url_for, session, g, jsonify
from app import app, db
from models import User, Offering, Course, Department, Term
# from flask_cas import login_required
from forms import EditForm, DeptPickerForm
from functools import wraps

SEASONS = ["W", "S", "X", "F"]

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('flask_cas.login'))

        return fn(*args, **kwargs)
    return wrapper

def year_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        if g.user.grad_year is None:
            return redirect(url_for('edit'))

    	return fn(*args, **kwargs)
    return wrapper

def add_terms(grad_year):
	for term in g.user.terms:
		g.user.remove_term(term)

	db.session.commit()

	# Add Freshman Fall
	t = Term.query.filter_by(year=grad_year - 4, season=SEASONS[3]).first()
	if t is None:
		t = Term(grad_year - 4, SEASONS[3])
		db.session.add(t)
	g.user.add_term(t)

	for year_diff in reversed(range(4)):
		for season in SEASONS:
			t = Term.query.filter_by(year=grad_year - year_diff, season=season).first()
			if t is None:
				t = Term(grad_year - year_diff, season)
				db.session.add(t)
			g.user.add_term(t)
	
	# Remove Extra Fall
	db.session.expunge(t)
	g.user.remove_term(t)

	
	db.session.commit()

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
        user = g.user)

@app.route('/planner', methods = ['GET'])
@login_required
@year_required
def planner():

	form = DeptPickerForm()

	form.dept_name.choices = [(a.id, a.abbr + " - " + a.name) for a in Department.query.order_by('abbr')]
	form.dept_name.choices.insert(0, (-1,"Choose a Department"))
	
	if form.validate_on_submit():
		flash('Your changes have been saved.')

	return render_template("planner.html",
        title = 'My Plan',
        user = g.user,
        form = form,
        courses = g.user.courses,
        terms = g.user.terms,
        off_terms = g.user.off_terms)

@app.route('/getcourses', methods = ['POST'])
@login_required
def getcourses():
	qryresult = Course.query.filter_by(department_id = request.form['dept'])

	j = jsonify( { 'courses' : [i.serialize for i in qryresult.order_by('number')] })

	return j

@app.route('/savecourse', methods = ['POST'])
@login_required
def savecourse():

	split_course = request.form["course_item"].strip().split(" ")

	d1 = Department.query.filter_by(abbr = split_course[0]).first()
	c1 = Course.query.filter_by(number = split_course[1], department = d1).first()

	year = "20" + request.form['term'][:2]
	season = request.form['term'][2]

	t = Term.query.filter_by(year = year, season = season).first()

	o1 = Offering.query.filter_by(course = c1, term = t).first()

	success = None
	if o1 is not None:
		success = g.user.take(o1)
	
	if success is None:
		j = jsonify( { 'error' : "Course could not be added" } )
		return j

	db.session.commit()

	j = jsonify( { 'name' : str(o1) } )

	return j

@app.route('/removecourse', methods = ['POST'])
@login_required
def removecourse():
	
	split_course = request.form["course"].strip().split(" ")

	d1 = Department.query.filter_by(abbr = split_course[0]).first()
	c1 = Course.query.filter_by(number = split_course[1], department = d1).first()
	
	year = "20" + request.form['term'][:2]
	season = request.form['term'][2]
	
	t = Term.query.filter_by(year = year, season = season).first()

	o1 = Offering.query.filter_by(course = c1, term = t).first()

	success = g.user.drop(o1)

	if not success:
		j = jsonify( { 'error' : "Course could not be added" } )
		return j

	db.session.commit()

	j = jsonify ( { 'error' : "", 'course' : str(o1) })

	return j

@app.route('/findterms', methods = ['POST'])
@login_required
def findterms():
	# Get Course
	split_course = request.form['course_item'].strip().split(" ")

	d1 = Department.query.filter_by(abbr = split_course[0]).first()
	c1 = Course.query.filter_by(number = split_course[1], department = d1).first()

	available_offerings = Offering.query.filter_by(course = c1)

	terms = []
	for offering in available_offerings:
		if offering.term not in terms:
			terms.append(offering.term)

	j = jsonify ( {} )
	if (terms != []):
		j = jsonify( { 'terms' : [i.serialize for i in terms] })

	return j

@app.route('/swapterm', methods = ['POST'])
@login_required
def swapterm():
	term_name = request.form['term']
	year = "20" + request.form['term'][:2]
	season = request.form['term'][2]

	t1 = Term.query.filter_by(year = year, season = season).first()

	g.user.swap_onterm(t1)
	db.session.commit()

	j = jsonify( {} )

	return j

@app.route('/settings')
@login_required
def settings():
	return redirect(url_for('user', netid = g.user.netid))

@app.route('/user/<netid>')
@login_required
def user(netid):
	user = User.query.filter_by(netid = netid).first()
	if user == None:
		flash('User ' + netid + ' not found.')
		return redirect(url_for('index'))
	return render_template('user.html',
		user = user)

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
	form = EditForm(g.user.nickname)
	if form.validate_on_submit():
		# if g.user.grad_year is None:
		add_terms(int(form.grad_year.data))

		g.user.nickname = form.nickname.data
		g.user.grad_year = form.grad_year.data
		db.session.add(g.user)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('planner'))
	else:
		form.nickname.data = g.user.nickname
		form.grad_year.data = g.user.grad_year
	return render_template('edit.html',
		form = form, user = g.user)
