# app/utils.py

import os
import PyPDF2
import re
import json
from openai import OpenAI
from app.models import Configuration, Candidate, RejectedCandidate
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

def check_requirements_ai(resume_text):
    """
    Uses AI to check if the resume meets the required criteria.
    Returns a tuple (meets_requirements, feedback).
    """
    prompt = f"""
You are an HR assistant helping to screen resumes.

Evaluate the following resume text to determine if the candidate meets the following requirements:
- GPA of 3.0 or higher. **If GPA is missing from the resume, consider it as not meeting the GPA requirement.**
- Knowledge of Python.

If the candidate does not meet any of the requirements, specify which requirement(s) is not met and provide a brief explanation.

Resume Text:
\"\"\"{resume_text}\"\"\"

Provide the evaluation in JSON format:
{{
  "meets_requirements": true or false,
  "feedback": "<Feedback explaining whether the candidate meets the requirements and why>"
}}
"""

    # Call OpenAI API
    try:
        response = client.chat.completions.create(
            model='gpt-4',
            messages=[
                {"role": "system", "content": "You are a helpful assistant that evaluates resumes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0
        )
    except Exception as e:
        current_app.logger.error(f"Error during OpenAI API call for resume screening: {e}")
        return False, 'Error during resume evaluation.'

    # Parse the response
    output = response.choices[0].message.content.strip()
    current_app.logger.info(f"AI Response for Resume Screening: {output}")
    # Remove code blocks or markdown formatting if necessary
    json_str = re.sub(r'```json|```', '', output).strip()
    # Parse JSON
    try:
        result = json.loads(json_str)
        meets_requirements_str = result.get('meets_requirements', False)
        # Convert to Boolean
        if isinstance(meets_requirements_str, bool):
            meets_requirements = meets_requirements_str
        elif isinstance(meets_requirements_str, str):
            meets_requirements = meets_requirements_str.lower() == 'true'
        else:
            meets_requirements = False
        feedback = result.get('feedback', '')
    except json.JSONDecodeError:
        current_app.logger.error("Failed to parse JSON from AI's response.")
        meets_requirements = False
        feedback = 'Error parsing AI response.'

    return meets_requirements, feedback

def evaluate_code(code, model='gpt-4'):
    # Fetch the selected model from the database or use the default
    config = Configuration.query.first()
    selected_model = config.openai_model if config and config.openai_model else model

    # Fetch recent developer feedbacks to use as examples
    recent_feedbacks = Candidate.query.filter(Candidate.developer_feedback != 'No comment').order_by(Candidate.date.desc()).limit(3).all()

    # Build few-shot examples
    examples = ''
    for candidate in recent_feedbacks:
        examples += f"Example code:\n{candidate.answers}\nFeedback:\n{candidate.developer_feedback}\n\n"

    messages = [
        {"role": "system", "content": "You are a senior software engineer evaluating code submissions. Provide output strictly in JSON format without any markdown or code block formatting."},
        {"role": "user", "content": f"""
Now evaluate the following Python code submitted by a candidate for correctness, efficiency, and code quality.

Candidate's code:
{code}

Evaluation criteria:
- Correctness: Does the code solve the problem correctly?
- Efficiency: Is the code optimized?
- Code Quality: Are there any syntax errors? Is the code readable and well-commented?

Provide the score, feedback, and issues in JSON format as follows:
{{
  "score": <score out of 100>,
  "feedback": "<feedback text>",
  "issues": ["<issue1>", "<issue2>", ...]
}}

Possible issues include:
- "syntax errors"
- "inefficient code"
- "poor readability"
- "no comments"
- "incorrect solution"
- "not valid python code"
- "invalid code"
- "does not solve any problem"
- "lacks any form of logic or structure"
- "optimization needed"
- "missing edge cases"
- "lack of error handling"
- "not optimized"
- "not readable"
- "not well-commented"
- "incomplete code"

Only include the issues that are present in the code. If there are no issues, provide an empty list for "issues": [].

Do not include any additional text, explanations, or formatting. Only provide the JSON response.
"""}
    ]

    try:
        response = client.chat.completions.create(
            model=selected_model,
            messages=messages,
            max_tokens=500,
            temperature=0
        )

        # Access content using dot notation
        output = response.choices[0].message.content.strip()
        current_app.logger.info(f"OpenAI API response: {output}")

        # Remove markdown code blocks if present
        json_str = re.sub(r'```json|```', '', output).strip()

        # Parse the JSON output
        try:
            result = json.loads(json_str)
            ai_score = int(result.get('score', 0))
            feedback = result.get('feedback', '').strip()
            issues = result.get('issues', [])
            final_score, passed, detailed_feedback = apply_grading_rubric(issues)
        except json.JSONDecodeError:
            current_app.logger.error("Failed to parse JSON from AI's response after cleaning.")
            final_score = 0
            feedback = 'Unable to evaluate the code.'
            passed = False
            detailed_feedback = feedback

    except Exception as e:
        current_app.logger.error(f"Error during OpenAI evaluation: {e}")
        final_score = 0
        feedback = 'Error during code evaluation.'
        passed = False
        detailed_feedback = feedback

    return final_score, passed, detailed_feedback

def apply_grading_rubric(issues):
    """
    Applies a grading rubric based on the list of issues to calculate the final score.
    """
    score = 100
    deductions = {
        'syntax errors': 10,
        'inefficient code': 5,
        'poor readability': 5,
        'no comments': 5,
        'incorrect solution': 20,
        'not valid python code': 50,
        'invalid code': 50,
        'does not solve any problem': 20,
        'lacks any form of logic or structure': 20,
        'optimization needed': 10,
        'missing edge cases': 10,
        'lack of error handling': 5,
        'not optimized': 5,
        'not readable': 5,
        'not well-commented': 5,
        'incomplete code': 50,
    }

    deduction_reasons = []
    for issue in issues:
        penalty = deductions.get(issue.lower(), 0)
        if penalty > 0:
            score -= penalty
            deduction_reasons.append(f"{issue.capitalize()} (-{penalty})")

    score = max(score, 0)
    passed = score >= 70
    detailed_feedback = f"Deductions: {', '.join(deduction_reasons)}" if deduction_reasons else "No deductions."

    return score, passed, detailed_feedback

def generate_overall_evaluation(resume_text, code, model='gpt-4'):
    """
    Uses AI to generate an overall evaluation combining the resume and code submission.
    The evaluation is a brief, balanced paragraph highlighting strengths and areas for improvement.
    Limited to 375 characters (~56 words).
    """
    prompt = f"""
You are an experienced HR specialist and software engineer. Based on the following resume and code submission, provide an overall evaluation of the candidate in a brief, constructive paragraph no longer than 375 characters (approximately 56 words).

Resume:
\"\"\"
{resume_text}
\"\"\"

Code Submission:
\"\"\"
{code}
\"\"\"

Provide your evaluation focusing on the candidate's skills, experience, and coding abilities. Highlight strengths and note areas for improvement in a supportive and encouraging manner.

Provide the evaluation in plain text without any additional formatting.
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that evaluates candidates based on their resume and code submission."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,  # Limit tokens to ensure brevity
            temperature=0.5  # Slight creativity for balanced feedback
        )

        # Get the AI's response
        overall_evaluation = response.choices[0].message.content.strip()
        current_app.logger.info(f"AI Overall Evaluation Response: {overall_evaluation}")

        # Truncate the evaluation to 375 characters if necessary
        if len(overall_evaluation) > 375:
            overall_evaluation = overall_evaluation[:372] + '...'

        current_app.logger.info(f"Truncated AI Overall Evaluation Response: {overall_evaluation}")

    except Exception as e:
        current_app.logger.error(f"Error during AI overall evaluation: {e}")
        overall_evaluation = 'Error generating overall evaluation.'

    return overall_evaluation
