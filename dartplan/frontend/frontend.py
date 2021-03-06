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

            return (redirect(url_for('frontend.edit')))
    else:
        g.user = None


# Default planner page for signed in users
@bp.route('/planner', methods=['GET'])
@login_required
@year_required
def planner():
    plan = g.user.plans.filter_by(default=True).first()
    return redirect(url_for('frontend.plan', plan_id=plan.id))


@bp.route('/plans/<int:plan_id>', methods=['GET'])
def plan(plan_id):
    plan = Plan.query.get_or_404(plan_id)

    # Check if terms aren't in the session
    if plan.terms.count() == 0:
        plan.reset_terms()

    return render_template('app.html',
                           title='%s - %s' % (plan.title, plan.user.nickname),
                           user=g.user)


@bp.route('/plans', methods=['GET'])
@login_required
@year_required
def plans():
    return render_template('app.html',
                           title='My Plans',
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

        localytics.track_profile(g.user.netid,
                                 {'grad_year': g.user.grad_year,
                                  'name': g.user.full_name,
                                  'email_course_updates':
                                  g.user.email_course_updates,
                                  'email_Dartplan_updates':
                                  g.user.email_Dartplan_updates
                                  })

        return redirect(url_for('frontend.plans'))
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
