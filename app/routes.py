# app/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from . import db
from .utils import allowed_file, parse_resume, check_requirements_ai, evaluate_code, generate_overall_evaluation
from werkzeug.utils import secure_filename
from datetime import datetime
from .models import Candidate, RejectedCandidate
import os
from flask import send_from_directory

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['resume']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            resume_text = parse_resume(filename)
            meets_requirements, feedback = check_requirements_ai(resume_text)
            if meets_requirements:
                # Store the resume filename and resume text in session
                session['resume_filename'] = filename
                session['resume_text'] = resume_text
                return redirect(url_for('main.assessment'))
            else:
                # Evaluate feedback to generate overall evaluation
                overall_evaluation = feedback  # Feedback from resume screening
                # Create a RejectedCandidate instance
                rejected_candidate = RejectedCandidate(
                    resume=filename,
                    score=0,  # Score is 0 for failed candidates
                    date=datetime.utcnow(),
                    developer_feedback='No comment',
                    overall_evaluation=overall_evaluation,
                    questions_asked='',
                    answers=''
                )
                db.session.add(rejected_candidate)
                db.session.commit()
                # Store feedback in session
                session['rejection_feedback'] = feedback
                return redirect(url_for('main.resume_rejection'))
    # For GET requests, render the resume upload form
    return render_template('resume_upload.html')

@main.route('/assessment', methods=['GET', 'POST'])
def assessment():
    # Define the question
    question_text = """
    Write a Python function that takes a list of integers and returns the list in reverse order.
    """

    if request.method == 'POST':
        submitted_code = request.form['code']
        score, passed, detailed_feedback = evaluate_code(submitted_code)
        current_app.logger.info(f"Evaluation Results - Score: {score}, Passed: {passed}, Feedback: {detailed_feedback}")
        resume_filename = session.get('resume_filename', 'Unknown')
        resume_text = session.get('resume_text', '')

        # Generate an overall evaluation using AI
        overall_evaluation = generate_overall_evaluation(resume_text, submitted_code)

        # Create a new Candidate instance and save data
        candidate = Candidate(
            resume=resume_filename,
            score=score,
            passed=passed,
            answers=submitted_code,
            date=datetime.utcnow(),
            developer_feedback='No comment',
            overall_evaluation=overall_evaluation,
            questions_asked=question_text.strip()
        )
        db.session.add(candidate)
        db.session.commit()
        # Store results in session for thank_you page
        session['score'] = score
        session['passed'] = passed
        session['feedback'] = detailed_feedback
        # Clear resume_text from session to free up space
        session.pop('resume_text', None)
        # Redirect to thank_you page
        return redirect(url_for('main.thank_you'))
    return render_template('assessment.html', question_text=question_text)

@main.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

# Admin Routes without authentication

@main.route('/admin/candidates')
def admin_candidates():
    # Fetch passed candidates
    passed_candidates = Candidate.query.filter(Candidate.passed == True).order_by(Candidate.date.desc()).all()
    # Fetch failed candidates
    failed_candidates = RejectedCandidate.query.order_by(RejectedCandidate.date.desc()).all()
    return render_template('admin_candidates.html', passed_candidates=passed_candidates, failed_candidates=failed_candidates)

@main.route('/admin/candidate/<int:candidate_id>/feedback', methods=['GET', 'POST'])
def add_developer_feedback(candidate_id):
    # Determine if the candidate is in Candidate or RejectedCandidate
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        candidate = RejectedCandidate.query.get(candidate_id)
    if not candidate:
        flash('Candidate not found.', 'danger')
        return redirect(url_for('main.admin_candidates'))
    if request.method == 'POST':
        developer_feedback = request.form.get('developer_feedback')
        if developer_feedback.strip() == '':
            developer_feedback = 'No comment'
        candidate.developer_feedback = developer_feedback
        db.session.commit()
        flash('Developer feedback updated successfully.', 'success')
        return redirect(url_for('main.admin_candidates'))
    return render_template('add_developer_feedback.html', candidate=candidate)

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@main.route('/resume_rejection')
def resume_rejection():
    feedback = session.get('rejection_feedback', 'Your application did not meet the required criteria.')
    return render_template('resume_rejection.html', feedback=feedback)
