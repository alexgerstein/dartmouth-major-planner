from . import bp

from flask import render_template, g, session, redirect, url_for
from functools import wraps

from dartplan.database import db
from dartplan.localytics import localytics
from dartplan.login import login_required
from dartplan.mail import welcome_notification
from dartplan.models import User, Plan
from dartplan.forms import UserEditForm


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
@bp.before_app_request
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


# Default planner page for signed in users
@bp.route('/planner', methods=['GET'])
@login_required
@year_required
def planner():
    plan = g.user.plans.first()
    return redirect(url_for('frontend.plan', plan_id=plan.id))


@bp.route('/plans/<int:plan_id>', methods=['GET'])
def plan(plan_id):
    plan = Plan.query.get_or_404(plan_id)

    # Check if terms aren't in the session
    if plan.terms.count() == 0:
        plan.reset_terms()

    return render_template('app.html',
                           title='%s Plan - %s' % (plan.title,
                                                   plan.user.nickname),
                           user=g.user)


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

        localytics.track_profile(g.user.net_id,
                                 {'grad_year': g.user.grad_year})

        plan = g.user.plans.first()
        plan.reset_terms()

        return redirect(url_for('frontend.planner'))
    return render_template('edit.html',
                           form=form, title='Edit Profile',
                           description="Change the nickname, graduation year, \
                           and email setting for your DARTPlan account.",
                           user=g.user)


@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('app.html', user=g.user)


@bp.app_errorhandler(401)
def unauthorized(error):
    return render_template('401.html', user=g.user), 401


@bp.app_errorhandler(500)
def server_error(error):
    return render_template('500.html', user=g.user), 500
