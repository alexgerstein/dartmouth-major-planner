from . import bp

from flask import render_template, g, session, redirect, url_for
from functools import wraps

from dartplan.database import db
from dartplan.login import login_required
from dartplan.mail import welcome_notification
from dartplan.models import User, Plan, Distributive, Hour, Department
from dartplan.forms import UserEditForm

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
        g.user.terms.remove(term)

    plan = g.user.plans.first()
    if plan:
        for term in plan.terms:
            plan.terms.remove(term)

    for term in terms:
        if term not in g.user.terms:
            g.user.terms.append(term)
        if plan:
            if term not in plan.terms:
                plan.terms.append(term)

    db.session.commit()


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

            plan = Plan(user_id=g.user.id)
            db.session.add(plan)
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

    all_terms = g.user.get_all_terms()

    dept_options = [{'key': dept.id, 'value': str(dept.abbr)}
                    for dept in Department.query.order_by('abbr')]
    hour_options = [{'key': hour.id, 'value': str(hour.period)}
                    for hour in Hour.query.order_by('id')]
    term_options = [{'key': term.id, 'value': str(term)} for term in all_terms]
    distrib_options = [{'key': distrib.id, 'value': str(distrib.abbr)}
                       for distrib in Distributive.query.order_by('abbr')]
    median_options = [{'key': index, 'value': str(median)}
                      for index, median in enumerate(MEDIANS)]

    # Check if terms aren't in the session
    if g.user.terms.all() == []:
        add_terms(all_terms)
        db.session.commit()

    return render_template("planner.html",
                           title='Course Plan',
                           user=g.user, dept_options=dept_options,
                           hour_options=hour_options,
                           term_options=term_options,
                           distrib_options=distrib_options,
                           median_options=median_options
                           )


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
        g.user.email_course_updates = form.email_course_updates.data
        g.user.email_Dartplan_updates = form.email_Dartplan_updates.data
        db.session.commit()

        add_terms(g.user.get_all_terms())
        db.session.commit()

        return redirect(url_for('frontend.planner'))
    else:
        # Reset form to current entries
        form.nickname.data = g.user.nickname
        form.grad_year.data = g.user.grad_year
        form.email_course_updates.data = g.user.email_course_updates
        form.email_Dartplan_updates.data = g.user.email_Dartplan_updates
    return render_template('edit.html',
                           form=form, title='Edit Profile',
                           description="Change the nickname, graduation year, \
                           and email setting for your DARTPlan account.",
                           user=g.user)


@bp.route('/')
@bp.route('/index')
def index():
    return render_template("index.html",
                           user_count=format(User.query.count(), ",d"),
                           user=g.user)


@bp.route('/about')
def about():
    return render_template("about.html",
                           user=g.user)


@bp.route('/disclaimer')
def disclaimer():
    return render_template("disclaimer.html",
                           user=g.user)


@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
