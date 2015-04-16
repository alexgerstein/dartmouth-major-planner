from . import bp

from flask import request, redirect, url_for, session, g, jsonify

from dartplan.database import db
from dartplan.login import login_required
from dartplan.models import User, Offering, Course, Department, Term, Hour, Distributive

MEDIANS = ['A', 'A/A-', 'A-', 'A-/B+', 'B+', 'B+/B', 'B', 'B/B-', 'B-', 'B-/C+', 'C+', 'C+/C', 'C']


# Helper method to get the offering a user is editing on the planner interface
def get_requested_offering(request):

    # Deconstruct the dragged item's id to get the course from the database
    if request.values.get('offering'):
        c1 = Offering.query.filter_by(id=request.values.get("offering")).first().get_course()
    else:
        c1 = Course.query.filter_by(id=request.values.get('course')).first()

    # Construct the requested offering based on where dropped
    year = "20" + request.values.get('term')[:2]
    season = request.values.get('term')[2]
    t = Term.query.filter_by(year=year, season=season).first()

    # Construct the requested hour if one exists
    if request.values.get('hour'):
        hour_string = request.values.get('hour')

        if hour_string == "Arr":
            hour_string = "Arrange"
        hour = Hour.query.filter_by(period=hour_string).first()
    else:
        offering = Offering.query.filter_by(course=c1, term=t).first()

        if offering is None:
            hour = Hour.query.filter_by(period="?").first()
        else:
            hour = offering.get_hour()

    o1 = Offering.query.filter_by(course=c1, term=t, hour=hour).first()
    if o1 is None:

        check_hour = Hour.query.filter_by(period="?").first()

        o1 = Offering(course=c1.id, term=t.id, hour=check_hour.id, desc="***User Added***<br>Consult registrar for more info", user_added="Y")
        db.session.add(o1)

        db.session.commit()

    return o1


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


# After change in dept form, send courses in that dept to user's view
@bp.route('/getcourses', methods=['GET'])
@login_required
def getcourses():

    courses = None
    for val in request.values.itervalues():
        if val != "-1":
            courses = Course.query.join(Offering)
            break

    if request.values.get('dept') != "-1":
        courses = courses.filter(Course.department_id == request.values.get('dept'))

    if request.values.get('term') != "-1":
        courses = courses.filter(Offering.term_id == request.values.get('term'))

    if request.values.get('hour') != "-1":
        courses = courses.filter(Offering.hour_id == request.values.get('hour'))

    if request.values.get('distrib') != "-1":
        distrib = Distributive.query.filter_by(id=int(request.values.get('distrib'))).first()
        courses = courses.filter(Offering.distributives.contains(distrib))

    if request.values.get('median') != '-1':
        courses = courses.filter(Course.avg_median.in_(MEDIANS[:int(request.values.get('median')) + 1]))

    if courses is None:
        j = jsonify({})
    else:
        j = jsonify({'courses': [i.serialize for i in courses.join(Department).order_by('abbr', 'number')]})

    return j


# If new course dragged into a box, store it in the user's courses
# Send the hour of the offering to the user
@bp.route('/savecourse', methods=['POST'])
@login_required
def savecourse():

    offering = get_requested_offering(request)

    success = None
    if offering is not None:
        success = g.user.take(offering)

    if success is None:
        j = jsonify({'error': "Course could not be added"})
        return j

    j = jsonify({'id': offering.id, 'name': str(offering), 'hour': str(offering.get_hour()), 'possible_hours': offering.get_possible_hours()})

    return j


# If user selects new hour from dropdown, update database.
@bp.route('/swaphour', methods=['POST'])
@login_required
def swaphour():

    offering = get_requested_offering(request)

    hour = Hour.query.filter_by(period=request.form['new_hour']).first()
    success = False
    if offering is not None:
        new_id = g.user.switch_hour(offering, hour)

    if not new_id:
        j = jsonify({'error': "Course could not be swapped"})
        return j

    j = jsonify({'id': new_id, 'name': str(offering), 'hour': str(hour), 'possible_hours': offering.get_possible_hours()})

    return j


# Callback to delete a course if user pressed red "Trash" button
@bp.route('/removecourse', methods=['POST'])
@login_required
def removecourse():

    offering = get_requested_offering(request)

    success = None
    if offering is not None:
        success = g.user.drop(offering)

    if not success:
        j = jsonify({'error': "Course could not be dropped"})
        return j

    j = jsonify({'error': "", 'course': str(offering)})

    return j


# Callback to see text of course offering
@bp.route('/getCourseInfo', methods=['GET'])
@login_required
def getCourseInfo():

    offering = get_requested_offering(request)

    return jsonify({"info": offering.desc})


# Callback to send all available terms of course so they can be highlighted on planner
@bp.route('/findterms', methods=['GET'])
@login_required
def findterms():

    # Get Course
    if request.values.get('offering'):

        c1 = Offering.query.filter_by(id=request.values.get('offering')).first().get_course()
    else:
        c1 = Course.query.filter_by(id=request.values.get('course')).first()

    available_user_offerings = Offering.query.filter_by(course=c1, user_added="Y").all()
    available_registrar_offerings = Offering.query.filter_by(course=c1, user_added="N").all()

    data = {'terms': [], 'user_terms': []}

    terms = {}
    for offering in available_registrar_offerings:
        if offering.term in terms:
            terms[str(offering.term)] += offering.get_user_count()
        else:
            terms[str(offering.term)] = offering.get_user_count()

    user_terms = {}
    for offering in available_user_offerings:
        if offering.term in user_terms:
            user_terms[str(offering.term)] += offering.get_user_count()
        else:
            user_terms[str(offering.term)] = offering.get_user_count()

    for key, value in terms.iteritems():
        data['terms'].append([key, value])

    for key, value in user_terms.iteritems():
        data['user_terms'].append([key, value])

    return jsonify(data)


# Callback to find all missing distribs
@bp.route('/missingdistribs', methods=['GET'])
@login_required
def getmissingdistribs():
    courses = sorted(g.user.courses, key=lambda offering: offering.distributives.count, reverse=True)
    missing_distribs = [str(distrib) for distrib in Distributive.query.all()]

    for course in courses:
        world_distrib = False
        general_distrib_taken = False

        for distrib in course.distributives.all():

            if distrib.abbr in missing_distribs:
                if distrib.abbr in ['CI', 'NW', 'W']:
                    if not world_distrib:
                        missing_distribs.remove(distrib.abbr)
                        world_distrib = True

                else:
                    if not general_distrib_taken:
                        missing_distribs.remove(distrib.abbr)
                        general_distrib_taken = True

                        # Remove paired lab/no-lab distribs
                        if distrib.abbr == 'SLA':
                            try:
                                missing_distribs.remove('SCI')
                            except ValueError:
                                pass
                        elif distrib.abbr == 'TLA':
                            try:
                                missing_distribs.remove('TAS')
                            except ValueError:
                                pass

            if general_distrib_taken and world_distrib:
                break

        # Check if lab is covered
        if 'TLA' not in missing_distribs:
            try:
                missing_distribs.remove('SLA')
            except ValueError:
                pass
        if 'SLA' not in missing_distribs:
            try:
                missing_distribs.remove('TLA')
            except ValueError:
                pass

    return jsonify({'missing': missing_distribs})


# Toggle on/off terms
@bp.route('/swapterm', methods=['POST'])
@login_required
def swapterm():

    # Get term from database
    term_name = request.form['term']
    year = "20" + term_name[:2]
    season = term_name[2]
    t1 = Term.query.filter_by(year=year, season=season).first()

    g.user.swap_onterm(t1)
    db.session.add(g.user)
    db.session.commit()

    j = jsonify({})

    return j


@bp.route('/edit/delete', methods=['GET', 'POST'])
@login_required
def delete_profile():
    db.session.delete(g.user)
    db.session.commit()
    session.pop('user', None)
    return redirect(url_for('frontend.index'))
