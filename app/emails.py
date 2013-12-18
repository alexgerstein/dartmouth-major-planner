#!../flask/bin/python

import imp

from flask.ext.mail import Message
from app import app, mail
from app.models import User
from flask import render_template, request
from config import ADMINS

from threading import Thread

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

@async
def send_async_email(msg):
    mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    
    send_async_email(msg)


def welcome_notification(user):
    send_email("%s, Welcome to DARTPlan!" % user.nickname.split(" ")[0],
        ADMINS[0],
        [user.netid + "@dartmouth.edu"],
        render_template("welcome_email.txt", 
            user = user),
        render_template("welcome_email.html", 
            user = user))

def updated_hour_notification(offering, new_hour):
    with app.test_request_context('http://dartplan.com/'):

        users = User.query.filter(User.courses.contains(offering)).all()

        for user in users:

            send_email("Nice call! %s (%s) now has an actual time." % (str(offering), str(offering.get_term())),
                ADMINS[0],
                [user.netid + "@dartmouth.edu"],
                render_template("updated_hour_email.txt",
                    user = user, offering = offering, new_hour = new_hour),
                render_template("updated_hour_email.html",
                    user = user, offering = offering, new_hour = new_hour))
