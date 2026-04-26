from models import db
from datetime import datetime

class StudyPreference(db.Model):
    __tablename__ = 'study_preferences'
    id = db.Column(db.Integer, primary_key=True)
    respondent_id = db.Column(db.Integer, db.ForeignKey('respondents.id'), nullable=False)
    kampus_diminati = db.Column(db.String(255))
    jurusan_diminati = db.Column(db.String(255))
    alasan_kuliah = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
