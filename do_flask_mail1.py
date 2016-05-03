#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
from flask_mail import Mail
from flask_mail import Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'penglee87@163.com'
app.config['MAIL_PASSWORD'] = '******'

mail = Mail(app)


msg = Message("Hello",
              sender="penglee87@163.com",
              recipients=["lipeng@qccr.com"])
msg.body = "testing"
msg.html = "<b>testing</b>"


with app.app_context():
    mail.send(msg)