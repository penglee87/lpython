#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
from flask_mail import Mail
from flask_mail import Message
import os

#测试成功,部分参数作用不明
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'penglee87@163.com'
app.config['MAIL_PASSWORD'] = '******'
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'  #邮件主题
#app.config['FLASKY_MAIL_SENDER'] = 'penglee87@163.com'
#app.config['FLASKY_ADMIN'] = 'penglee87@163.com'
mail = Mail(app)
"""
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
"""

@app.route("/")
def index():
    #Message(主题,发件人,收件人)
    msg = Message("Hello",
                  sender="penglee87@163.com",
                  recipients=["lipeng@qccr.com"])
                  
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    mail.send(msg)
    return '<h1>Hello World!</h1>'
    
    
if __name__ == '__main__':
    app.run(debug=True)
    
    
    
"""
msg = Message("Hello",
              sender="penglee87@163.com",
              recipients=["lipeng@qccr.com"])
msg.body = "testing"
msg.html = "<b>testing</b>"

mail.send(msg)

if __name__ == '__main__':
    mail.send(msg)
    

pip install --no-deps lamson chardet flask-mail
set MAIL_USERNAME=penglee87@163.com
set MAIL_PASSWORD=******
set FLASKY_ADMIN=penglee87@163.com


>>> from flask.ext.mail import Message
>>> from hello import mail
>>> msg = Message('test subject', sender='penglee1206@gmail.com',recipients=['380517767@qq.com'])
>>> msg.body = 'text body'
>>> msg.html = '<b>HTML</b> body'
>>> with app.app_context():
...     mail.send(msg)

"""