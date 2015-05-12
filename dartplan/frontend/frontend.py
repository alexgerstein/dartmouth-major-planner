from . import bp

from flask import render_template, g, session, redirect, url_for
from functools import wraps

from dartplan.database import db
from dartplan.login import login_required
from dartplan.mail import welcome_notification
from dartplan.models import User, Term, Distributive, Hour, Department
from dartplan.forms import UserEditForm, DeptPickerForm, HourPickerForm, \
                           TermPickerForm, DistribPickerForm, MedianPickerForm

SEASONS = ["W", "S", "X", "F"]
MEDIANS = ['A', 'A/A-', 'A-', 'A-/B+', 'B+', 'B+/B', 'B',
           'B/B-', 'B-', 'B-/C+', 'C+', 'C+/C', 'C']


# Wrapper to make sure students can't view planner without giving it its range
def year_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        if g.user.grad_year is None:
            return redirect(url_for('frontend.edit'))

        return fn(*args, **kwargs)
    return wrapper


# If graduation year changes for user, adjusts terms in planner
def add_terms(terms):

    # Clear all terms, start clean
    for term in g.user.terms:
        g.user.remove_term(term)
        db.session.commit()

    for term in terms:
        g.user.add_term(term)
        db.session.commit()


def generate_terms(grad_year):
    all_terms = []

    # Add Freshman Fall
    t = Term.query.filter_by(year=grad_year - 4, season=SEASONS[3]).first()
    if t is None:
        t = Term(year=grad_year - 4, season=SEASONS[3])
        db.session.add(t)

    all_terms.append(t)

    for year_diff in reversed(range(4)):
        for season in SEASONS:
            t = Term.query.filter_by(year=grad_year - year_diff, season=season).first()
            if t is None:
                t = Term(year=grad_year - year_diff, season=season)
                db.session.add(t)

            all_terms.append(t)

    # Remove extra fall
    all_terms.remove(t)

    return all_terms


# Always track if there is a current user signed in
# If unrecognized user is in, add them to user database
@bp.before_request
def fetch_user():

    if 'user' in session:
        g.user = User.query.filter_by(netid=session['user']['netid']).first()
        if g.user is None:
            g.user = User(session['user']['name'], session['user']['netid'])
            db.session.add(g.user)
            db.session.commit()

            return (redirect(url_for('frontend.edit')))
    else:
        g.user = None


# Planner page for signed in users
# Landing Page for All Users, most will be redirected to login form
@bp.route('/planner', methods=['GET'])
@login_required
@year_required
def planner():

    all_terms = generate_terms(g.user.grad_year)

    # Initialize the department selection form
    dept_form = DeptPickerForm()
    dept_form.dept_name.choices = [(a.id, a.abbr + " - " + a.name) for a in Department.query.order_by('abbr')]
    dept_form.dept_name.choices.insert(0, (-1, "Select Department"))

    # Initialize the hour selection form
    hour_form = HourPickerForm()
    hour_form.hour_name.choices = [(a.id, a.period) for a in Hour.query.order_by('id')]
    hour_form.hour_name.choices.insert(0, (-1, "Select Hour"))

    # Initialize the term selection form
    term_form = TermPickerForm()
    term_form.term_name.choices = [(a.id, str(a)) for a in all_terms]
    term_form.term_name.choices.insert(0, (-1, "Select Term"))

    # Initialize the term selection form
    distrib_form = DistribPickerForm()
    distrib_form.distrib_name.choices = [(a.id, str(a)) for a in Distributive.query.order_by('abbr')]
    distrib_form.distrib_name.choices.insert(0, (-1, "Select Distrib"))

    median_form = MedianPickerForm()
    median_form.median_name.choices = [(index, str(a)) for index, a in enumerate(MEDIANS)]
    median_form.median_name.choices.insert(0, (-1, 'Select Min. Median'))

    # Check if terms aren't in the session
    if g.user.terms.all() == []:
        add_terms(all_terms)
        db.session.commit()

    return render_template("planner.html",
                           title='Course Plan',
                           description='Manage your Dartmouth course plan \
                           with simple drag-and-drop functionality.',
                           user=g.user, dept_form=dept_form,
                           hour_form=hour_form, term_form=term_form,
                           distrib_form=distrib_form, median_form=median_form,
                           courses=g.user.courses.order_by('hour_id'),
                           on_terms=g.user.terms.order_by('year', 'id').all(),
                           terms=all_terms)


# Edit Page to change Name and Graduation Year
@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = UserEditForm(g.user.nickname)

    if form.validate_on_submit():

        g.user.nickname = form.nickname.data

        # Send welcome email if new user
        if g.user.grad_year is None:
            welcome_notification(g.user)

        g.user.grad_year = form.grad_year.data
        g.user.email_course_updates = form.course_updates.data
        g.user.email_Dartplan_updates = form.dartplan_updates.data

        add_terms(generate_terms(form.grad_year.data))
        db.session.commit()

        return redirect(url_for('frontend.planner'))
    else:
        # Reset form to current entries
        form.nickname.data = g.user.nickname
        form.grad_year.data = g.user.grad_year
        form.course_updates.data = g.user.email_course_updates
        form.dartplan_updates.data = g.user.email_Dartplan_updates
    return render_template('edit.html',
                           form=form, title='Edit Profile',
                           description="Change the nickname, graduation year, \
                           and email setting for your DARTPlan account.",
                           user=g.user)


# Settings redirect's to user's own profile page
@bp.route('/settings')
@login_required
def settings():
    return render_template('user.html', title='Settings',
                           description="View the settings for your DARTPlan \
                           account.", user=g.user)


@bp.route('/')
@bp.route('/index')
def index():
    return render_template("index.html",
                           user_count=format(User.query.count(), ",d"))


@bp.route('/about')
def about():
    return render_template("about.html")


@bp.route('/about/contact')
def contact():
    return render_template("contact.html")


@bp.route('/about/donate')
def donate():
    return render_template("donate.html")


@bp.route('/about/contribute')
def contribute():
    return render_template("contribute.html")


@bp.route('/about/disclaimer')
def disclaimer():
    return render_template("disclaimer.html")


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
