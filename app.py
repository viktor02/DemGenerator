import json
import logging
import os
import random
import string
from time import gmtime, strftime

import flask
from flask import Flask, flash, request, redirect, url_for, render_template
from simpledemotivators import Demotivator, Quote
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

app = Flask(__name__)
application = app

app.config.from_file('config.json', load=json.load)
logging.basicConfig(level=logging.WARNING, filename='log.txt')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route('/view/<name>')
def view_dem(name):
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
        # Check if fields empty
        if (request.form.get('text') == "") or (request.form.get('subtext') == ""):
            flash('No selected text')
            return redirect(request.url)
        # Check if fields too long
        if (len(request.form.get('text')) >= 255) or (len(request.form.get('subtext')) >= 255):
            flash('Too long text')
            return redirect(request.url)
        # If everything okay
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            inp_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(inp_filepath)

            out_filename = id_generator() + ".jpg"
            out_filepath = os.path.join(app.config['OUT_FOLDER'], out_filename)

            choice = request.form.get('select')
            if choice == '1':
                is_check_watermark = request.form.get('watermark')
                dem = Demotivator(request.form.get('text'), request.form.get('subtext'))
                if is_check_watermark == '1':
                    dem.create(inp_filepath,
                               fonttext=app.config['FONT_PATH'],
                               RESULT_FILENAME=out_filepath,
                               line=app.config['WATERMARK'])
                else:
                    dem.create(inp_filepath,
                               fonttext=app.config['FONT_PATH'],
                               RESULT_FILENAME=out_filepath)
            elif choice == '2':
                quote = Quote(request.form.get('text'), request.form.get('subtext'))
                quote.get(inp_filepath,
                          name_font=app.config['FONT_PATH'],
                          text_font=app.config['FONT_PATH'],
                          headline_font=app.config['FONT_PATH'],
                          RESULT_FILENAME=out_filepath)
            else:
                flash('Select error')
                return redirect(request.url)

            logging.warning(f"{strftime('%Y-%m-%d %H:%M:%S', gmtime())} - {flask.request.remote_addr} - {filename}")

            return redirect(url_for('view_dem', name=out_filename))
    return render_template('index.html')
