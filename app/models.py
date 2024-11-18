# app/models.py

from . import db
from datetime import datetime

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume = db.Column(db.String(200), nullable=False)
    passed = db.Column(db.Boolean, default=True)
    score = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    developer_feedback = db.Column(db.Text, default='No comment')
    overall_evaluation = db.Column(db.Text)
    questions_asked = db.Column(db.Text)
    answers = db.Column(db.Text)

    def __repr__(self):
        return f'<Candidate {self.id}>'

class RejectedCandidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume = db.Column(db.String(200), nullable=False)
    passed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    developer_feedback = db.Column(db.Text, default='No comment')
    overall_evaluation = db.Column(db.Text)
    questions_asked = db.Column(db.Text, default='')
    answers = db.Column(db.Text, default='')

    def __repr__(self):
        return f'<RejectedCandidate {self.id}>'

class Configuration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    openai_model = db.Column(db.String(50), nullable=False, default='gpt-4')

    def __repr__(self):
        return f'<Configuration {self.openai_model}>'

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    ideal_answer = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20))  # 'Easy', 'Medium', 'Hard'

    def __repr__(self):
        return f'<Question {self.id}>'
