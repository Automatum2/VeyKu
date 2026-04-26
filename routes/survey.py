from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import db
from models.respondent import Respondent
from models.survey_response import SurveyResponse

survey_bp = Blueprint('survey', __name__)

QUESTIONS = [
    {'id': 1, 'title': 'Pemecahan Masalah', 'question': 'Saat menghadapi sebuah masalah atau tantangan baru, bagaimana pendekatan utama Anda?',
     'options': [{'value': 'Teknik & IT', 'emoji': '🧩', 'text': 'Menganalisis logika kerjanya dan merancang solusi yang sistematis.'},
                 {'value': 'Sains & Medis', 'emoji': '🔬', 'text': 'Mencari tahu penyebab dasarnya melalui riset dan observasi mendalam.'},
                 {'value': 'Bisnis & Manajemen', 'emoji': '🎯', 'text': 'Mencari peluang keuntungan dan menyusun strategi agar lebih efisien.'},
                 {'value': 'Seni & Desain', 'emoji': '✨', 'text': 'Memikirkan solusi kreatif yang belum pernah dipikirkan orang lain.'},
                 {'value': 'Sosial & Humaniora', 'emoji': '🤝', 'text': 'Mempertimbangkan dampak dan solusinya terhadap orang-orang di sekitar.'}]},
                 
    {'id': 2, 'title': 'Kenyamanan Kerja', 'question': 'Kondisi lingkungan atau gaya bekerja seperti apa yang membuat Anda paling nyaman?',
     'options': [{'value': 'Teknik & IT', 'emoji': '💻', 'text': 'Bekerja dengan perangkat, mesin, atau teknologi canggih secara mandiri.'},
                 {'value': 'Sains & Medis', 'emoji': '🧪', 'text': 'Lingkungan yang tenang, terstruktur, objektif, dan berbasis data.'},
                 {'value': 'Bisnis & Manajemen', 'emoji': '🚀', 'text': 'Dinamis, penuh kompetisi yang sehat, dan berorientasi pada target.'},
                 {'value': 'Seni & Desain', 'emoji': '🎨', 'text': 'Suasana yang fleksibel, tidak kaku, dan memberikan kebebasan berekspresi.'},
                 {'value': 'Sosial & Humaniora', 'emoji': '🗣️', 'text': 'Tempat di mana saya bisa banyak berinteraksi, berdiskusi, dan membantu orang.'}]},
                 
    {'id': 3, 'title': 'Peran Proyek', 'question': 'Jika Anda diberi sebuah proyek besar, bagian mana yang paling ingin Anda kerjakan?',
     'options': [{'value': 'Teknik & IT', 'emoji': '⚙️', 'text': 'Membangun infrastruktur atau mengurus sistem teknisnya dari nol.'},
                 {'value': 'Sains & Medis', 'emoji': '📊', 'text': 'Mengumpulkan data, menguji teori, atau memastikan keakuratan informasi.'},
                 {'value': 'Bisnis & Manajemen', 'emoji': '💼', 'text': 'Memimpin tim, mengatur anggaran, dan mempresentasikan hasil akhir.'},
                 {'value': 'Seni & Desain', 'emoji': '🖌️', 'text': 'Merancang tampilan visual, estetika, atau elemen kreatif dari proyek tersebut.'},
                 {'value': 'Sosial & Humaniora', 'emoji': '👥', 'text': 'Memastikan proyek tersebut tepat sasaran dan memahami respons audiensnya.'}]},
                 
    {'id': 4, 'title': 'Kekuatan Diri', 'question': 'Apa kekuatan alami terbesar yang Anda miliki saat menyerap informasi baru?',
     'options': [{'value': 'Teknik & IT', 'emoji': '🧠', 'text': 'Sangat cepat memahami pola, logika, dan cara kerja suatu benda/sistem.'},
                 {'value': 'Sains & Medis', 'emoji': '🔎', 'text': 'Sangat teliti pada detail dan mampu menganalisis fakta yang rumit/abstrak.'},
                 {'value': 'Bisnis & Manajemen', 'emoji': '💡', 'text': 'Cepat melihat nilai jual atau bagaimana hal itu bisa menguntungkan.'},
                 {'value': 'Seni & Desain', 'emoji': '👁️', 'text': 'Mudah membayangkan dan memvisualisasikan ide tersebut ke dalam bentuk karya.'},
                 {'value': 'Sosial & Humaniora', 'emoji': '📝', 'text': 'Pintar merangkum, berkomunikasi, dan menyampaikannya agar mudah dipahami orang lain.'}]},
                 
    {'id': 5, 'title': 'Minat Topik', 'question': 'Jika Anda harus membaca artikel atau menonton film dokumenter, topik apa yang paling menarik perhatian Anda?',
     'options': [{'value': 'Teknik & IT', 'emoji': '🤖', 'text': 'Inovasi teknologi masa depan, robotika, atau kemajuan artificial intelligence.'},
                 {'value': 'Sains & Medis', 'emoji': '🧬', 'text': 'Misteri alam semesta, penemuan ilmiah, atau rahasia anatomi manusia.'},
                 {'value': 'Bisnis & Manajemen', 'emoji': '📈', 'text': 'Biografi tokoh sukses, kisah perusahaan dunia, atau strategi ekonomi.'},
                 {'value': 'Seni & Desain', 'emoji': '🎭', 'text': 'Sejarah seni, arsitektur dunia, pameran desain, atau pertunjukan budaya.'},
                 {'value': 'Sosial & Humaniora', 'emoji': '🌍', 'text': 'Peristiwa sejarah, psikologi manusia, atau dinamika masyarakat modern.'}]},
                 
    {'id': 6, 'title': 'Dana Pengembangan Diri', 'question': 'Jika Anda punya dana khusus untuk hobi atau pengembangan diri, Anda akan membelanjakannya untuk apa?',
     'options': [{'value': 'Teknik & IT', 'emoji': '🖥️', 'text': 'Gadget terbaru, komponen komputer, atau lisensi software.'},
                 {'value': 'Sains & Medis', 'emoji': '🔬', 'text': 'Buku ensiklopedia tebal, mikroskop, atau peralatan eksperimen.'},
                 {'value': 'Bisnis & Manajemen', 'emoji': '💰', 'text': 'Modal merintis usaha kecil, saham, atau tiket seminar bisnis.'},
                 {'value': 'Seni & Desain', 'emoji': '📷', 'text': 'Kamera profesional, alat gambar berkualitas, atau tiket pameran seni.'},
                 {'value': 'Sosial & Humaniora', 'emoji': '🤝', 'text': 'Kegiatan donasi, acara komunitas, atau pelatihan public speaking.'}]},
                 
    {'id': 7, 'title': 'Menghadapi Aturan', 'question': 'Bagaimana cara Anda merespons sebuah aturan atau prosedur kerja yang sangat kaku?',
     'options': [{'value': 'Teknik & IT', 'emoji': '⚡', 'text': 'Mencari cara mengotomasinya menggunakan teknologi agar lebih cepat.'},
                 {'value': 'Sains & Medis', 'emoji': '📏', 'text': 'Mematuhi prosedur tersebut selama alasan logis dan ilmiahnya terbukti.'},
                 {'value': 'Bisnis & Manajemen', 'emoji': '🤝', 'text': 'Bernegosiasi dengan atasan untuk mencari efisiensi biaya dan waktu.'},
                 {'value': 'Seni & Desain', 'emoji': '🕊️', 'text': 'Merasa terkekang dan mencoba mencari cara agar bisa lebih fleksibel.'},
                 {'value': 'Sosial & Humaniora', 'emoji': '⚖️', 'text': 'Mempertanyakan apakah aturan tersebut adil bagi semua orang yang terlibat.'}]},
                 
    {'id': 8, 'title': 'Fokus Berita', 'question': 'Saat membaca sebuah berita atau kejadian besar, aspek apa yang pertama kali Anda perhatikan?',
     'options': [{'value': 'Teknik & IT', 'emoji': '🏗️', 'text': 'Teknologi atau infrastruktur yang digunakan dalam peristiwa tersebut.'},
                 {'value': 'Sains & Medis', 'emoji': '📊', 'text': 'Fakta objektif, statistik, dan penyebab riil kejadian tersebut.'},
                 {'value': 'Bisnis & Manajemen', 'emoji': '📉', 'text': 'Dampak ekonomi, naik-turunnya saham, atau kerugian finansial yang terjadi.'},
                 {'value': 'Seni & Desain', 'emoji': '📸', 'text': 'Foto, ilustrasi visual, atau estetika media dalam mengemas cerita tersebut.'},
                 {'value': 'Sosial & Humaniora', 'emoji': '❤️', 'text': 'Dampak psikologis dan kesejahteraan masyarakat yang terkena dampaknya.'}]},
                 
    {'id': 9, 'title': 'Reaksi Kegagalan', 'question': 'Saat sebuah proyek kelompok gagal total, apa reaksi spontan Anda?',
     'options': [{'value': 'Teknik & IT', 'emoji': '🔧', 'text': 'Membongkar ulang sistemnya untuk mencari cacat teknis atau "bug".'},
                 {'value': 'Sains & Medis', 'emoji': '🔍', 'text': 'Mengumpulkan ulang data untuk melihat variabel mana yang keliru.'},
                 {'value': 'Bisnis & Manajemen', 'emoji': '🔄', 'text': 'Menghitung kerugian dan menyusun rencana darurat (pivot) secepat mungkin.'},
                 {'value': 'Seni & Desain', 'emoji': '🗑️', 'text': 'Membuang konsep lama dan mencari inspirasi untuk karya yang benar-benar baru.'},
                 {'value': 'Sosial & Humaniora', 'emoji': '🤗', 'text': 'Mengumpulkan anggota tim untuk evaluasi dan saling menguatkan mental.'}]},
                 
    {'id': 10, 'title': 'Kegiatan Sukarela', 'question': 'Jika Anda diwajibkan menjadi sukarelawan (volunteer), Anda akan memilih tugas sebagai apa?',
     'options': [{'value': 'Teknik & IT', 'emoji': '🌐', 'text': 'Memperbaiki jaringan komputer atau membuat website untuk panti asuhan.'},
                 {'value': 'Sains & Medis', 'emoji': '🚑', 'text': 'Menjadi asisten tenaga medis di posko kesehatan masyarakat.'},
                 {'value': 'Bisnis & Manajemen', 'emoji': '📦', 'text': 'Menjadi ketua panitia penggalangan dana atau koordinator logistik.'},
                 {'value': 'Seni & Desain', 'emoji': '🎨', 'text': 'Membuat poster kampanye, mendekorasi ruangan, atau tim dokumentasi foto.'},
                 {'value': 'Sosial & Humaniora', 'emoji': '🎓', 'text': 'Menjadi pengajar sukarela atau konselor bagi anak-anak di pedalaman.'}]},
                 
    {'id': 11, 'title': 'Hobi Masa Kecil', 'question': 'Kilas balik ke masa kecil, mainan/hobi apa yang paling sering membuat Anda lupa waktu?',
     'options': [{'value': 'Teknik & IT', 'emoji': '🎮', 'text': 'Membongkar radio bekas, merakit Lego Technic, atau main video game.'},
                 {'value': 'Sains & Medis', 'emoji': '🦖', 'text': 'Bermain dengan kit eksperimen anak, teleskop, atau ensiklopedia dinosaurus.'},
                 {'value': 'Bisnis & Manajemen', 'emoji': '🎲', 'text': 'Bermain Monopoli, berjualan mainan ke teman, atau game strategi membangun kota.'},
                 {'value': 'Seni & Desain', 'emoji': '🖍️', 'text': 'Menggambar, mewarnai, bermain plastisin (playdough), atau melipat origami.'},
                 {'value': 'Sosial & Humaniora', 'emoji': '🎭', 'text': 'Bermain peran (roleplay) seperti dokter-dokteran atau asyik mendengarkan dongeng.'}]},
                 
    {'id': 12, 'title': 'Gaya Mengajar', 'question': 'Saat Anda harus menjelaskan konsep yang sangat rumit kepada teman, cara apa yang Anda gunakan?',
     'options': [{'value': 'Teknik & IT', 'emoji': '📈', 'text': 'Menggunakan diagram alur (flowchart) atau langkah-langkah yang terstruktur.'},
                 {'value': 'Sains & Medis', 'emoji': '📚', 'text': 'Menyebutkan referensi ahli, buku, dan membeberkan fakta-fakta ilmiahnya.'},
                 {'value': 'Bisnis & Manajemen', 'emoji': '⚡', 'text': 'Langsung *to-the-point* ke kesimpulan dan apa untung-ruginya.'},
                 {'value': 'Seni & Desain', 'emoji': '🖼️', 'text': 'Menggunakan perumpamaan visual, sketsa, atau gambar agar lebih menarik.'},
                 {'value': 'Sosial & Humaniora', 'emoji': '📖', 'text': 'Memakai analogi cerita kehidupan sehari-hari agar lebih mengena di hati.'}]},
                 
    {'id': 13, 'title': 'Adaptasi Lingkungan Baru', 'question': 'Ketika masuk ke lingkungan yang benar-benar baru (sekolah/kantor baru), apa yang Anda lakukan?',
     'options': [{'value': 'Teknik & IT', 'emoji': '🔌', 'text': 'Mencari tahu cara kerja fasilitas atau letak sistem koneksi di gedung tersebut.'},
                 {'value': 'Sains & Medis', 'emoji': '🧐', 'text': 'Mengamati dari kejauhan, menganalisis pola interaksi orang sebelum berbaur.'},
                 {'value': 'Bisnis & Manajemen', 'emoji': '🤝', 'text': 'Mencari tahu siapa orang paling penting (leader) dan mencoba membangun koneksi awal.'},
                 {'value': 'Seni & Desain', 'emoji': '🏛️', 'text': 'Memperhatikan detail interior ruangan, tata cahaya, dan suasana estetikanya.'},
                 {'value': 'Sosial & Humaniora', 'emoji': '👋', 'text': 'Langsung tersenyum, menyapa, dan mengajak ngobrol orang di sebelah untuk keakraban.'}]},
                 
    {'id': 14, 'title': 'Keputusan Penting', 'question': 'Apa parameter paling krusial bagi Anda dalam mengambil keputusan hidup yang besar?',
     'options': [{'value': 'Teknik & IT', 'emoji': '⏱️', 'text': 'Efisiensi, rasionalitas, dan apakah keputusan ini sistematis untuk jangka panjang.'},
                 {'value': 'Sains & Medis', 'emoji': '⚖️', 'text': 'Objektivitas data pendukung dan persentase minim risiko fatal.'},
                 {'value': 'Bisnis & Manajemen', 'emoji': '📈', 'text': 'Return of Investment (ROI), potensi pertumbuhan karir, dan keamanan finansial.'},
                 {'value': 'Seni & Desain', 'emoji': '🎨', 'text': 'Orisinalitas, nilai keindahan, dan apakah ini membatasi kebebasan berekspresi saya.'},
                 {'value': 'Sosial & Humaniora', 'emoji': '🕊️', 'text': 'Keharmonisan, keselarasan dengan nurani, dan tidak merugikan orang banyak.'}]},
                 
    {'id': 15, 'title': 'Definisi Sukses', 'question': 'Apa definisi kesuksesan hidup atau "legacy" menurut Anda pribadi?',
     'options': [{'value': 'Teknik & IT', 'emoji': '🚀', 'text': 'Menciptakan teknologi atau inovasi yang dipakai dan memudahkan jutaan umat manusia.'},
                 {'value': 'Sains & Medis', 'emoji': '🎓', 'text': 'Menemukan obat, teori baru, atau berkontribusi pada pengetahuan dasar peradaban.'},
                 {'value': 'Bisnis & Manajemen', 'emoji': '👑', 'text': 'Membangun kerajaan usaha yang besar, bebas finansial, dan menjadi pemimpin industri.'},
                 {'value': 'Seni & Desain', 'emoji': '🖼️', 'text': 'Karya saya diakui sebagai mahakarya, dipamerkan, dan menginspirasi generasi baru.'},
                 {'value': 'Sosial & Humaniora', 'emoji': '🌍', 'text': 'Mampu mengubah kebijakan sosial, mendidik bangsa, atau menyelamatkan masyarakat lemah.'}]}
]

@survey_bp.route('/')
def landing():
    return render_template('survey/landing.html')

@survey_bp.route('/data-diri', methods=['GET', 'POST'])
def data_diri():
    if request.method == 'POST':
        nis = request.form.get('nis', '').strip()
        nama = request.form.get('nama', '').strip()
        jurusan_smk = request.form.get('jurusan_smk', '').strip()
        email = request.form.get('email', '').strip()
        no_wa = request.form.get('no_wa', '').strip()
        
        if not all([nis, nama, jurusan_smk, email, no_wa]):
            flash('Semua field harus diisi!', 'error')
            return render_template('survey/data_diri.html')
            
        # Cek apakah NIS sudah ada di database
        existing_respondent = Respondent.query.filter_by(nis=nis).first()
        if existing_respondent:
            flash(f'NIS {nis} sudah pernah mengisi survei! NIS tidak boleh sama.', 'error')
            return render_template('survey/data_diri.html')
            
        session['respondent_data'] = {
            'nis': nis,
            'nama': nama,
            'jurusan_smk': jurusan_smk,
            'email': email,
            'no_wa': no_wa
        }
        session['answers'] = {}
        return redirect(url_for('survey.questions'))
    return render_template('survey/data_diri.html')

@survey_bp.route('/pertanyaan', methods=['GET', 'POST'])
def questions():
    if 'respondent_data' not in session:
        return redirect(url_for('survey.data_diri'))
        
    if request.method == 'POST':
        data = request.get_json()
        if data:
            q_id = str(data.get('question_id'))
            answer = data.get('answer')
            
            # Validasi jawaban
            valid_options = []
            for q in QUESTIONS:
                if str(q['id']) == q_id:
                    valid_options = [opt['value'] for opt in q['options']]
                    break
                    
            if answer in valid_options:
                answers = session.get('answers', {})
                answers[q_id] = answer
                session['answers'] = answers
                return jsonify({'status': 'ok', 'next': int(q_id) < len(QUESTIONS)})
                
        return jsonify({'status': 'error'}), 400
        
    return render_template('survey/questions.html', questions=QUESTIONS)

@survey_bp.route('/hasil')
def result():
    if 'respondent_data' not in session or 'answers' not in session:
        return redirect(url_for('survey.data_diri'))
        
    answers = session.get('answers', {})
    if len(answers) < len(QUESTIONS):
        flash('Kamu belum menjawab semua pertanyaan!', 'error')
        return redirect(url_for('survey.questions'))
        
    resp_data = session['respondent_data']
    
    # Hitung skor (5 Rumpun)
    skor = {
        'Teknik & IT': 0,
        'Sains & Medis': 0,
        'Bisnis & Manajemen': 0,
        'Seni & Desain': 0,
        'Sosial & Humaniora': 0
    }
    
    for q_id, answer in answers.items():
        if answer in skor:
            skor[answer] += 1
            
    # Tentukan rumpun pemenang
    pemenang = max(skor, key=skor.get)
    jurusan_smk = resp_data['jurusan_smk']
    
    # Simpan Respondent
    respondent = Respondent(
        nis=resp_data['nis'],
        nama=resp_data['nama'], 
        jurusan_smk=jurusan_smk,
        email=resp_data['email'], 
        no_wa=resp_data['no_wa']
    )
    db.session.add(respondent)
    db.session.flush()
    
    # Simpan SurveyResponse
    survey = SurveyResponse(
        respondent_id=respondent.id,
        skor_teknik=skor['Teknik & IT'],
        skor_medis=skor['Sains & Medis'],
        skor_bisnis=skor['Bisnis & Manajemen'],
        skor_seni=skor['Seni & Desain'],
        skor_soshum=skor['Sosial & Humaniora'],
        hasil_rekomendasi=pemenang
    )
    db.session.add(survey)
    db.session.commit()
    
    # Cleanup session
    nama = resp_data['nama']
    for k in ['respondent_data','answers']:
        session.pop(k, None)
        
    DAFTAR_JURUSAN = {
        'Teknik & IT': ['Ilmu Komputer', 'Teknik Informatika', 'Sistem Informasi', 'Teknik Sipil', 'Teknik Mesin', 'Teknik Elektro', 'Teknik Industri', 'Arsitektur'],
        'Sains & Medis': ['Kedokteran', 'Farmasi', 'Keperawatan', 'Kesehatan Masyarakat', 'Biologi', 'Kimia', 'Matematika', 'Ilmu Gizi'],
        'Bisnis & Manajemen': ['Manajemen Bisnis', 'Akuntansi', 'Ilmu Ekonomi', 'Bisnis Digital', 'Administrasi Bisnis', 'Pemasaran', 'Keuangan'],
        'Seni & Desain': ['Desain Komunikasi Visual (DKV)', 'Desain Interior', 'Seni Rupa', 'Animasi', 'Tata Busana', 'Perfilman & Televisi', 'Seni Musik'],
        'Sosial & Humaniora': ['Psikologi', 'Ilmu Komunikasi', 'Hubungan Internasional', 'Hukum', 'Sastra Inggris', 'Ilmu Politik', 'Sosiologi']
    }
    
    rekomendasi_jurusan = DAFTAR_JURUSAN.get(pemenang, [])
    
    # Logika Keselarasan
    rumpun_smk_map = {
        'DPIB': 'Teknik & IT',
        'TKP': 'Teknik & IT',
        'TPM': 'Teknik & IT',
        'TKR': 'Teknik & IT',
        'TSM': 'Teknik & IT',
        'TPTUP': 'Teknik & IT',
        'TITL': 'Teknik & IT',
        'TAV': 'Teknik & IT',
        'TKJ': 'Teknik & IT',
        'RPL': 'Teknik & IT',
        'DKV': 'Seni & Desain',
        'PRF': 'Seni & Desain'
    }
    
    rumpun_asal = rumpun_smk_map.get(jurusan_smk, 'Lainnya')
    is_selaras = (rumpun_asal == pemenang)
    
    return render_template('survey/result.html', hasil=pemenang, skor=skor, nama=nama, total_soal=len(QUESTIONS), rekomendasi_jurusan=rekomendasi_jurusan, jurusan_smk=jurusan_smk, is_selaras=is_selaras)

@survey_bp.route('/statistik')
def statistik():
    # Menghitung total data
    total_responden = Respondent.query.count()
    
    # Menghitung per rumpun
    t_teknik = SurveyResponse.query.filter_by(hasil_rekomendasi='Teknik & IT').count()
    t_medis = SurveyResponse.query.filter_by(hasil_rekomendasi='Sains & Medis').count()
    t_bisnis = SurveyResponse.query.filter_by(hasil_rekomendasi='Bisnis & Manajemen').count()
    t_seni = SurveyResponse.query.filter_by(hasil_rekomendasi='Seni & Desain').count()
    t_soshum = SurveyResponse.query.filter_by(hasil_rekomendasi='Sosial & Humaniora').count()
    
    return render_template('survey/statistik.html',
                           total_responden=total_responden,
                           t_teknik=t_teknik,
                           t_medis=t_medis,
                           t_bisnis=t_bisnis,
                           t_seni=t_seni,
                           t_soshum=t_soshum)

@survey_bp.route('/about')
def about():
    return render_template('survey/about.html')
