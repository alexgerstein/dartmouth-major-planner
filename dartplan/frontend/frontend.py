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
    plan = g.user.plans.first()

    # Check if terms aren't in the session
    if plan.terms.count() == 0:
        plan.reset_terms()

    dept_options = [{'key': dept.id, 'value': str(dept.abbr)}
                    for dept in Department.query.order_by('abbr')]
    hour_options = [{'key': hour.id, 'value': str(hour.period)}
                    for hour in Hour.query.order_by('id')]
    term_options = [{'key': term.id, 'value': str(term)}
                    for term in plan.terms]
    distrib_options = [{'key': distrib.id, 'value': str(distrib.abbr)}
                       for distrib in Distributive.query.order_by('abbr')]
    median_options = [{'key': index, 'value': str(median)}
                      for index, median in enumerate(MEDIANS)]

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
    form = UserEditForm(obj=g.user)

    if form.validate_on_submit():
        # Send welcome email if new user
        if g.user.grad_year is None:
            welcome_notification(g.user)

        form.populate_obj(g.user)
        db.session.commit()

        plan = g.user.plans.first()
        plan.reset_terms()

        return redirect(url_for('frontend.planner'))
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
