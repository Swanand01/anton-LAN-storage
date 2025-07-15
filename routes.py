from flask import request, session, redirect, url_for, render_template, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
import shutil

from decorators import login_required
from utils import get_unique_name, get_icon_filename


def register_routes(app, storage_dir, username, password):
    @app.route('/')
    @app.route('/<path:subpath>')
    @login_required
    def index(subpath=''):
        full_path = os.path.join(storage_dir, subpath)
        if not os.path.isdir(full_path):
            return 'Not a folder', 404

        sort = request.args.get('sort', 'name-asc')

        entries = []
        for entry in os.listdir(full_path):
            abs_path = os.path.join(full_path, entry)
            is_folder = os.path.isdir(abs_path)
            mtime = os.path.getmtime(abs_path)
            size = os.path.getsize(abs_path) if not is_folder else None
            icon = get_icon_filename(entry, is_folder)

            entries.append({
                'name': entry,
                'is_folder': is_folder,
                'mtime': mtime,
                'size': size,
                'icon': icon,
            })

        reverse = 'desc' in sort
        if 'date' in sort:
            entries.sort(key=lambda e: (
                not e['is_folder'], e['mtime']), reverse=reverse)
        else:
            entries.sort(key=lambda e: (
                not e['is_folder'], e['name'].lower()), reverse=reverse)

        return render_template(
            'index.html',
            entries=entries,
            current_path=subpath,
            current_sort=sort,
        )

    @app.route('/upload', methods=['POST'])
    @login_required
    def upload():
        file = request.files.get('file')
        path = request.form.get('path', '')
        if not file or file.filename == '':
            return 'No file selected', 400
        raw_name = secure_filename(file.filename)
        filename = get_unique_name(os.path.join(storage_dir, path), raw_name)
        full_path = os.path.join(storage_dir, path)
        os.makedirs(full_path, exist_ok=True)
        file.save(os.path.join(full_path, filename))
        return '', 204

    @app.route('/download/<path:file_path>')
    @login_required
    def download(file_path):
        folder = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        return send_from_directory(os.path.join(storage_dir, folder), filename, as_attachment=True)

    @app.route('/delete/<path:file_path>', methods=['POST'])
    @login_required
    def delete(file_path):
        full_path = os.path.join(storage_dir, file_path)
        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)
        else:
            return 'Not found', 404
        return '', 204

    @app.route('/mkdir', methods=['POST'])
    @login_required
    def make_dir():
        raw_name = request.form.get('name', '').strip()
        path = request.form.get('path', '')
        if not raw_name:
            return 'No folder name', 400

        base_path = os.path.join(storage_dir, path)
        unique_name = get_unique_name(base_path, secure_filename(raw_name))
        os.makedirs(os.path.join(base_path, unique_name), exist_ok=True)
        return redirect(url_for('index', subpath=path))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            if request.form['username'] == username and request.form['password'] == password:
                session['logged_in'] = True
                return redirect(url_for('index'))
            flash('Invalid credentials')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        session.pop('logged_in', None)
        return redirect(url_for('login'))
