from app import create_app
from models import db
from models.user import User
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("Menghapus tabel versi lama secara paksa (termasuk tabel usang)...")
    with db.engine.connect() as connection:
        # Gunakan CASCADE untuk PostgreSQL agar tabel yang memiliki relasi bisa dihapus
        connection.execute(text('DROP TABLE IF EXISTS work_preferences CASCADE;'))
        connection.execute(text('DROP TABLE IF EXISTS study_preferences CASCADE;'))
        connection.execute(text('DROP TABLE IF EXISTS survey_responses CASCADE;'))
        connection.execute(text('DROP TABLE IF EXISTS respondents CASCADE;'))
        connection.execute(text('DROP TABLE IF EXISTS users CASCADE;'))
        connection.commit()
    
    print("Membuat tabel versi MajorMind Blue...")
    db.create_all()
    
    # Buat ulang admin
    admin = User(name='Admin Veyku', email='admin@veyku.com', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    
    print("Selesai! Database kini sudah punya kolom asal_sekolah, skor_teknik, dll.")
