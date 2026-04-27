from models import db
from datetime import datetime

class Respondent(db.Model):
    __tablename__ = 'respondents'
    
    id = db.Column(db.Integer, primary_key=True)
    nis = db.Column(db.String(20), nullable=False, unique=True)
    nama = db.Column(db.String(100), nullable=False)
    jurusan_smk = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    no_wa = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    survey_response = db.relationship('SurveyResponse', backref='respondent', uselist=False, cascade='all, delete-orphan')
