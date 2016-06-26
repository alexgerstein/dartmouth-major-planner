#!../flask/bin/python

from flask_mail import Message, Mail
from flask import render_template

import logging

mail = Mail()
logger = logging.getLogger('DARTplan')

ADMINS = ['support@dartplan.com']


def create_message(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    return msg


def welcome_notification(user):
    logger.info("NEW USER %s" % user.nickname)
    message = create_message("%s, Welcome to DARTPlan!" % user.nickname.split(" ")[0],
        ADMINS[0],
        [user.email()],
        render_template("emails/welcome_email.txt", user=user),
        render_template("emails/welcome_email.html", user=user))

    mail.send(message)


def updated_hour_notification(users, offering, new_hour):
    for user in users:

        logger.info("EMAIL UPDATED OFFERING TO %s FROM" % user.nickname)
        message = create_message("Nice call! %s (%s) now has an actual time." % (str(offering), str(offering.term)),
                ADMINS[0],
                [user.email()],
                render_template("emails/updated_hour_email.txt",
                    user=user, offering=offering, new_hour=new_hour),
                render_template("emails/updated_hour_email.html",
                    user=user, offering=offering, new_hour=new_hour))

        mail.send(message)


def swapped_course_times(users, offering, other_time):
    for user in users:
        logger.info("EMAIL SWAPPED OFFERING TO %s ABOUT %s AT %s FOR %s" % (user.nickname, offering, offering.hour, other_time.hour))
        message = create_message("The ol' switcheroo... %s seems to be at a new time." % (str(offering)),
                ADMINS[0],
                [user.email()],
                render_template("emails/swapped_email.txt",
                    user=user, old_offering=offering, new_offering=other_time),
                render_template("emails/swapped_email.html",
                    user=user, old_offering=offering, new_offering=other_time))

        mail.send(message)


def deleted_offering_notification(users, offering, term, hour):
    for user in users:
        logger.info("EMAIL DELETED OFFERING TO %s ABOUT %s AT %s" % (user.nickname, offering, hour))
        message = create_message("Oh no! %s is no longer offered when you thought it would be." % (str(offering)),
                ADMINS[0],
                [user.email()],
                render_template("emails/deleted_email.txt",
                    user=user, offering=offering, term=term, hour=hour),
                render_template("emails/deleted_email.html",
                    user=user, offering=offering, term=term, hour=hour))

        mail.send(message)
