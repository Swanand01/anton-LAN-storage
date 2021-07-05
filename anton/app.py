import os
from flask import Flask, request, redirect, url_for, send_file, session
from flask.templating import render_template
from flask_autoindex import AutoIndex

from werkzeug.utils import redirect, secure_filename
from zipfile import ZipFile
from os.path import basename


ppath = 'shared'

app = Flask(__name__)
app.config['UPLOAD_PATH'] = ppath
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

idx = AutoIndex(app, browse_root=ppath, add_url_rules=False)


@app.route('/', methods=['GET', 'POST'])
def login():
    password = request.form.get("password")
    print(password, type(password))
    if password == "1234":
        session["logged_in"] = True
        return redirect(url_for('autoindex'))
    else:
        session["logged_in"] = False
        return render_template('__autoindex__/login.html')


@app.route('/files', methods=['GET', 'POST'])
@app.route('/files/<path:path>', methods=['GET', 'POST'])
def autoindex(path='.'):
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file[]")
        for uploaded_file in uploaded_files:
            filename = secure_filename(uploaded_file.filename)
            if filename != '':
                uploaded_file.save(os.path.join(
                    app.config['UPLOAD_PATH'], filename))
    if session["logged_in"] == True:
        return idx.render_autoindex(path)
    else:
        return redirect(url_for('login'))


@app.route('/delete/<path:path>')
def delete(path):
    file = path.split('/')[1]
    os.remove(ppath + "\\" + file)
    return redirect(url_for('autoindex'))


@app.route('/zip', methods=['POST'])
def zip():
    name = request.form.get('zipname')
    zip_files = request.files.getlist("dir[]")
    for file in zip_files:
        filename = secure_filename(file.filename)
        if filename != '':
            file.save(os.path.join('zips', filename))
    if len(os.listdir('zips')) != 0:
        zipObj = ZipFile(f'shared/{name}.zip', 'w')
        for folderName, subfolders, filenames in os.walk('zips'):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, basename(filePath))
        for f in os.listdir('zips'):
            os.remove(os.path.join('zips', f))
    return redirect(url_for('autoindex'))


@app.route('/download/<path:path>')
def downloadFile(path):
    file = path.split('/')[1]
    return send_file(ppath + "\\" + file, as_attachment=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
