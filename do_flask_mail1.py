#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config.update(
    MAIL_SERVER='smtp.qq.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='380517767@qq.com',
    MAIL_PASSWORD='******',  # 使用QQ邮箱的授权码
)

mail = Mail(app)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

@app.route('/send_email')
def send_email_route():
    subject = "flask Email Title"
    sender = "380517767@qq.com"
    recipients = ["penglee87@163.com"]
    text_body = "this is a flask test email"
    html_body = "<h1>this is a flask test email</h1>"

    send_email(subject, sender, recipients, text_body, html_body)

    return "email send success"

if __name__ == '__main__':
    app.run(debug=True)

'''
运行后,打开浏览器访问 http://127.0.0.1:5000/send_email
'''
