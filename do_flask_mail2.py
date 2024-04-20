#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask_mail import Mail, Message
from threading import Thread

app = Flask(__name__)

# 从环境变量中读取配置信息
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.qq.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 465))
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'True').lower() in ['true', '1']
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '380517767@qq.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '******')  #使用QQ邮箱的授权码

mail = Mail(app)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    return msg

def async_send_email(app, msg):
    with app.app_context():
        mail.send(msg)

@app.route('/send_email')
def send_email_route():
    subject = "Flask Email Title"
    sender = "380517767@qq.com"
    recipients = ["penglee87@163.com"]
    text_body = "This is a Flask test email"
    html_body = "<h1>This is a Flask test email</h1>"

    msg = send_email(subject, sender, recipients, text_body, html_body)

    # 使用线程异步发送邮件
    thr = Thread(target=async_send_email, args=(app, msg))
    thr.start()

    return "Email send success"

if __name__ == '__main__':
    app.run(debug=True)
