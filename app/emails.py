import threading

from flask import render_template, copy_current_request_context, current_app
from flask.ext.mail import Message
from app import mail
from config import ADMINS

# @async
# def send_async_email(msg):
#     with current_app.test_request_context() as request:
        

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body

    @copy_current_request_context
    def send_message(message):
        mail.send(msg)
    
    sender = threading.Thread(target=send_message, args=(msg))
    sender.start()

def welcome_notification(user):
    send_email("%s, Welcome to DARTPlan!" % user.nickname.split(" ")[0],
        ADMINS[0],
        [user.netid + "@dartmouth.edu"],
        render_template("welcome_email.txt", 
            user = user),
        render_template("welcome_email.html", 
            user = user))