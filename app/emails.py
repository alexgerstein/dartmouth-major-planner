#!../flask/bin/python

import imp

from flask.ext.mail import Message, Mail
from app import app
from flask import render_template, request, copy_current_request_context
from config import ADMINS

from threading import Thread

mail = Mail()

# def async(f):
#     def wrapper(*args, **kwargs):
#         thr = Thread(target = f, args = args, kwargs = kwargs)
#         thr.start()
#     return wrapper

# @async
# def send_async_email(msg):
#     mail.send(msg)

def create_message(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    
    return msg


def welcome_notification(user):

    app.logger.info("NEW USER %s" % user.nickname)
    message = create_message("%s, Welcome to DARTPlan!" % user.nickname.split(" ")[0],
        ADMINS[0],
        [user.netid + "@dartmouth.edu"],
        render_template("welcome_email.txt", 
            user = user),
        render_template("welcome_email.html", 
            user = user))

    @copy_current_request_context
    def send_message(message):
        mail.send(message)

    sender = Thread(name='emails', target=send_message, args=(message,))
    sender.start()

def updated_hour_notification(users, offering, new_hour):
        with app.test_request_context():
            for user in users:

                app.logger.info("EMAIL UPDATED OFFERING TO %s FROM" % user.nickname)
                message = create_message("Nice call! %s (%s) now has an actual time." % (str(offering), str(offering.get_term())),
                        ADMINS[0],
                        [user.netid + "@dartmouth.edu"],
                        render_template("updated_hour_email.txt",
                            user = user, offering = offering, new_hour = new_hour),
                        render_template("updated_hour_email.html",
                            user = user, offering = offering, new_hour = new_hour))

                @copy_current_request_context
                def send_message(message):
                   mail.send(message)

                sender = Thread(name='emails', target=send_message, args=(message,))
                sender.start()

def deleted_offering_notification(users, offering, term, hour):
        with app.test_request_context():
            for user in users:
                app.logger.info("EMAIL DELETED OFFERING TO %s ABOUT %s AT %s" % (user.nickname, offering, hour))
                message = create_message("Oh no! %s is no longer offered when you thought it would be." % (str(offering)),
                        ADMINS[0],
                        [user.netid + "@dartmouth.edu"],
                        render_template("deleted_email.txt",
                            user = user, offering = offering, term = term, hour = hour),
                        render_template("deleted_email.html",
                            user = user, offering = offering, term = term, hour = hour))

                @copy_current_request_context
                def send_message(message):
                    mail.send(message)

                sender = Thread(name='emails', target=send_message, args=(message,))
                sender.start()
