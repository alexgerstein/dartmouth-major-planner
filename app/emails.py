from flask.ext.mail import Message
from app import mail
from flask import render_template
from config import ADMINS

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def welcome_notification(user):
    send_email("%s, Welcome to DARTPlan!" % user.nickname.split(" ")[0],
        ADMINS[0],
        [user.netid + "@dartmouth.edu"],
        render_template("welcome_email.txt", 
            user = user),
        render_template("welcome_email.html", 
            user = user))