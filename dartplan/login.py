# Adapted from Dartmouth Hacker Club

from flask import Blueprint, request, redirect, session, url_for
import urllib
import requests
from lxml import etree
from functools import wraps

flask_cas = Blueprint('flask_cas', __name__, template_folder='templates')

CAS_URL = 'https://login.dartmouth.edu/cas/'


# Wrapper function so certain pages remain private to new users
def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('flask_cas.login'))

        return fn(*args, **kwargs)
    return wrapper


def recursive_dict(element):
    return element.tag, dict(map(recursive_dict, element)) or element.text


def cas_login(service):
    login_url = CAS_URL + 'login?' + urllib.urlencode(locals())
    return redirect(login_url)


def cas_validate(ticket, service):
    validate_url = CAS_URL + 'serviceValidate?' + urllib.urlencode(locals())
    r = requests.get(validate_url)
    doc = etree.fromstring(r.text)
    if 'authenticationSuccess' in doc[0].tag:
        return dict((key.replace('{http://www.yale.edu/tp/cas}', ''), value) for \
                key, value in recursive_dict(doc[0])[1].items())
    return None


@flask_cas.route("/login")
def login():
    callback_url = request.url.split('?')[0]
    if 'ticket' in request.args:
        session['user'] = cas_validate(request.args['ticket'], callback_url)
    else:
        return cas_login(callback_url)

    return redirect(url_for('frontend.planner'))


@flask_cas.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for("frontend.index"))
