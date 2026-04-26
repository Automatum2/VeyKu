from models import db
from datetime import datetime

class SurveyResponse(db.Model):
    __tablename__ = 'survey_responses'
    id = db.Column(db.Integer, primary_key=True)
    respondent_id = db.Column(db.Integer, db.ForeignKey('respondents.id'), nullable=False)
    
    # Skor 5 Rumpun Jurusan
    skor_teknik = db.Column(db.Integer, nullable=False, default=0)
    skor_medis = db.Column(db.Integer, nullable=False, default=0)
    skor_bisnis = db.Column(db.Integer, nullable=False, default=0)
    skor_seni = db.Column(db.Integer, nullable=False, default=0)
    skor_soshum = db.Column(db.Integer, nullable=False, default=0)
    
    hasil_rekomendasi = db.Column(db.String(100), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
