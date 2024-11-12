# app/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from . import db
from .utils import allowed_file, parse_resume, check_requirements, evaluate_code
from werkzeug.utils import secure_filename
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['resume']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            resume_text = parse_resume(filename)
            if check_requirements(resume_text):
                return redirect(url_for('main.assessment'))
            else:
                flash('Resume does not meet the required criteria.')
                return redirect(request.url)
    return render_template('resume_upload.html')

@main.route('/assessment', methods=['GET', 'POST'])
def assessment():
    if request.method == 'POST':
        submitted_code = request.form['code']
        score, passed, feedback = evaluate_code(submitted_code)
        if passed:
            return redirect(url_for('main.thank_you'))
        else:
            flash(f'Code evaluation failed with score: {score}. Feedback: {feedback}')
            return redirect(request.url)
    return render_template('assessment.html')

@main.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')
