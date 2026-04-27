from models import db
from datetime import datetime

class WorkPreference(db.Model):
    __tablename__ = 'work_preferences'
    id = db.Column(db.Integer, primary_key=True)
    respondent_id = db.Column(db.Integer, db.ForeignKey('respondents.id'), nullable=False)
    bidang_diminati = db.Column(db.String(100))
    alasan_kerja = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
