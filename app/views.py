from flask import render_template, flash, redirect, url_for, session, g
from app import app, db
from models import User
from flask_cas import login_required
from forms import EditForm

@app.before_request
def fetch_user():

	if 'user' in session:
		g.user = User.query.filter_by(netid=session['user']['netid']).first()
		if g.user is None:
			g.user = User(session['user']['name'], session['user']['netid'])
			db.session.add(g.user)
			db.session.commit()
	else:
		g.user = None

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html",
        title = 'Home',
        user = g.user)

@app.route('/planner')
@login_required
def planner():
	return render_template("planner.html",
        title = 'My Plan',
        user = g.user)

@app.route('/settings')
@login_required
def settings():
	return redirect(url_for('user', netid = g.user.netid))

@app.route('/user/<netid>')
@login_required
def user(netid, page = 1):
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
		g.user.nickname = form.nickname.data
		g.user.grad_year = form.grad_year.data
		db.session.add(g.user)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit'))
	else:
		form.nickname.data = g.user.nickname
		form.grad_year.data = g.user.grad_year
	return render_template('edit.html',
		form = form)
