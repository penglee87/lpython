#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
flask 实现文件上传
"""
import os
from flask import Flask, request, redirect, url_for
from flask import send_from_directory
from werkzeug import secure_filename
from werkzeug import SharedDataMiddleware

UPLOAD_FOLDER = r'C:\\'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  #限制文件大小

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        print('type(file)',type(file))
        print('file.filename',type(file.filename),file.filename)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print('filename',type(filename),filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
    </form>
    '''
    

#读取已上传文件的内容
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

'''
app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']})
'''
                               
if __name__ == '__main__':
    app.run(debug=True)