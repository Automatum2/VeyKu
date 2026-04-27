from flask import Blueprint, render_template, request, send_file
from flask_login import login_required, current_user
from models import db
from models.respondent import Respondent
from models.survey_response import SurveyResponse
from sqlalchemy import desc

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@login_required
def dashboard():
    # Menghitung total data
    total_responden = Respondent.query.count()
    
    # Menghitung per rumpun
    t_teknik = SurveyResponse.query.filter_by(hasil_rekomendasi='Teknik & IT').count()
    t_medis = SurveyResponse.query.filter_by(hasil_rekomendasi='Sains & Medis').count()
    t_bisnis = SurveyResponse.query.filter_by(hasil_rekomendasi='Bisnis & Manajemen').count()
    t_seni = SurveyResponse.query.filter_by(hasil_rekomendasi='Seni & Desain').count()
    t_soshum = SurveyResponse.query.filter_by(hasil_rekomendasi='Sosial & Humaniora').count()
    
    return render_template('admin/dashboard.html',
                           total_responden=total_responden,
                           t_teknik=t_teknik,
                           t_medis=t_medis,
                           t_bisnis=t_bisnis,
                           t_seni=t_seni,
                           t_soshum=t_soshum,
                           admin_name=current_user.name)

@admin_bp.route('/responden')
@login_required
def responden_list():
    page = request.args.get('page', 1, type=int)
    # Menampilkan 20 responden per halaman
    pagination = Respondent.query.order_by(desc(Respondent.created_at)).paginate(page=page, per_page=20)
    
    return render_template('admin/respondents.html', pagination=pagination)

@admin_bp.route('/responden/<int:id>')
@login_required
def responden_detail(id):
    respondent = Respondent.query.get_or_404(id)
    survey = SurveyResponse.query.filter_by(respondent_id=id).first()
    
    return render_template('admin/respondent_detail.html', 
                           respondent=respondent, 
                           survey=survey)
