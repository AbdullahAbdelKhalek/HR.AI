# app/utils.py

import os
import PyPDF2
import re
from openai import OpenAI  # Import the new OpenAI client
from app.models import Configuration
from flask import current_app
from dotenv import load_dotenv
from . import db

ALLOWED_EXTENSIONS = {'pdf'}

# Load environment variables from .env
load_dotenv()

# Initialize the OpenAI client with the API key
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=openai_api_key)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_resume(filename):
    """
    Extracts text from a PDF resume using PyPDF2's PdfReader.
    """
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    resume_text = ''
    try:
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    resume_text += text
    except Exception as e:
        current_app.logger.error(f"Error parsing resume: {e}")
        raise e
    return resume_text

def check_requirements(resume_text):
    """
    Checks if the resume meets the required criteria:
    - GPA over 3.0
    - Knowledge of Python
    """
    gpa_match = re.search(r'GPA[:\s]*([0-9]\.[0-9])', resume_text, re.IGNORECASE)
    python_knowledge = 'python' in resume_text.lower()

    if gpa_match:
        try:
            gpa = float(gpa_match.group(1))
        except ValueError:
            gpa = 0.0
    else:
        gpa = 0.0

    meets_gpa = gpa >= 3.0
    meets_python = python_knowledge

    return meets_gpa and meets_python

def apply_grading_rubric(feedback):
    """
    Applies a grading rubric to the AI's feedback to calculate the final score.
    """
    score = 100
    deductions = {
        'syntax error': 10,
        'inefficient code': 5,
        'poor readability': 5,
        'no comments': 5,
        'incorrect solution': 20,
        'optimization needed': 10,
        'missing edge cases': 10,
        'lack of error handling': 5,
    }

    feedback_lower = feedback.lower()
    for issue, penalty in deductions.items():
        if issue in feedback_lower:
            score -= penalty

    score = max(score, 0)
    passed = score >= 70

    return score, passed

def evaluate_code(code, model='gpt-3.5-turbo'):
    """
    Evaluates the submitted code using the specified OpenAI model.
    Default model is 'gpt-3.5-turbo'.
    """
    # Fetch the selected model from the database or use the default
    config = Configuration.query.first()
    selected_model = config.openai_model if config and config.openai_model else model

    # Validate the model name
    valid_models = ['gpt-3.5-turbo', 'gpt-4']
    if selected_model not in valid_models:
        current_app.logger.warning(
            f"Model '{selected_model}' is not valid. Using default model '{model}'."
        )
        selected_model = model

    messages = [
        {"role": "system", "content": "You are a senior software engineer."},
        {"role": "user", "content": f"""
Evaluate the following Python code submitted by a candidate for correctness, efficiency, and code quality. Provide a score out of 100 and a brief feedback.

Candidate's code:
{code}

Evaluation criteria:
- Correctness: Does the code solve the problem correctly?
- Efficiency: Is the code optimized?
- Code Quality: Are there any syntax errors? Is the code readable and well-commented?

Provide the score and feedback in the following format:
Score: <score>
Feedback: <feedback>
"""}
    ]

    try:
        response = client.chat.completions.create(
            model=selected_model,
            messages=messages,
            max_tokens=200,
            temperature=0
        )

        # Access content using dot notation
        output = response.choices[0].message.content.strip()
        score_match = re.search(r'Score:\s*(\d+)', output)
        feedback_match = re.search(r'Feedback:\s*(.*)', output, re.DOTALL)

        if score_match and feedback_match:
            ai_score = int(score_match.group(1))
            feedback = feedback_match.group(1).strip()
            final_score, passed = apply_grading_rubric(feedback)
        else:
            final_score = 0
            feedback = 'Unable to evaluate the code.'
            passed = False

    except Exception as e:
        current_app.logger.error(f"Error during OpenAI evaluation: {e}")
        final_score = 0
        feedback = 'Error during code evaluation.'
        passed = False

    return final_score, passed, feedback
