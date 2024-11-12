# app/models.py

from . import db
from datetime import datetime

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer)
    passed = db.Column(db.Boolean)
    answers = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Candidate {self.id}>'

class Configuration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    openai_model = db.Column(db.String(50), nullable=False, default='text-davinci-003')

    def __repr__(self):
        return f'<Configuration {self.openai_model}>'
