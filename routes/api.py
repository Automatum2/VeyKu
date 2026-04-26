from flask import Blueprint, jsonify
from flask_login import login_required
from models import db
from models.survey_response import SurveyResponse
from models.respondent import Respondent
from sqlalchemy import func

api_bp = Blueprint('api', __name__)

@api_bp.route('/stats/general')
@login_required
def general_stats():
    # Mengambil data untuk chart utama (pie chart hasil rekomendasi)
    kerja = SurveyResponse.query.filter_by(hasil='kerja').count()
    kuliah = SurveyResponse.query.filter_by(hasil='kuliah').count()
    seimbang = SurveyResponse.query.filter_by(hasil='seimbang').count()
    
    return jsonify({
        'labels': ['Kerja', 'Kuliah', 'Seimbang'],
        'data': [kerja, kuliah, seimbang],
        'colors': ['#00e3fd', '#de8eff', '#ac89ff']
    })

@api_bp.route('/stats/jurusan')
@login_required
def jurusan_stats():
    # Mengambil data distribusi rekomendasi berdasarkan jurusan
    results = db.session.query(
        Respondent.jurusan,
        SurveyResponse.hasil,
        func.count(SurveyResponse.id)
    ).join(SurveyResponse).group_by(Respondent.jurusan, SurveyResponse.hasil).all()
    
    # Format data untuk stacked bar chart
    jurusan_dict = {}
    for jurusan, hasil, count in results:
        if jurusan not in jurusan_dict:
            jurusan_dict[jurusan] = {'kerja': 0, 'kuliah': 0, 'seimbang': 0}
        jurusan_dict[jurusan][hasil] = count
        
    labels = list(jurusan_dict.keys())
    data_kerja = [jurusan_dict[j]['kerja'] for j in labels]
    data_kuliah = [jurusan_dict[j]['kuliah'] for j in labels]
    data_seimbang = [jurusan_dict[j]['seimbang'] for j in labels]
    
    return jsonify({
        'labels': labels,
        'datasets': [
            {'label': 'Kerja', 'data': data_kerja, 'backgroundColor': '#00e3fd'},
            {'label': 'Kuliah', 'data': data_kuliah, 'backgroundColor': '#de8eff'},
            {'label': 'Seimbang', 'data': data_seimbang, 'backgroundColor': '#ac89ff'}
        ]
    })
