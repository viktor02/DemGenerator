import os
import pathlib
import random
import string

import flask
from flask import Flask, flash, request, redirect, url_for, render_template
from simpledemotivators import Demotivator
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = str(pathlib.Path('uploaded'))
OUT_FOLDER = str(pathlib.Path('generated'))
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
application = app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUT_FOLDER'] = OUT_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route('/view/<name>')
def view_dem(name):
    # return render_template('generated.html', filename=name)
    return flask.send_from_directory(app.config["OUT_FOLDER"], name)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            inp_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(inp_filepath)

            out_filename = id_generator() + ".jpg"
            out_filepath = os.path.join(app.config['OUT_FOLDER'], out_filename)

            dem = Demotivator(request.form.get('text'), request.form.get('subtext'))
            dem.create(inp_filepath, RESULT_FILENAME=out_filepath)

            return redirect(url_for('view_dem', name=out_filename))
    return render_template('index.html')
