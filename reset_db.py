from app import create_app
from models import db
from models.user import User
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("Menghapus tabel versi lama secara paksa (termasuk tabel usang)...")
    with db.engine.connect() as connection:
        connection.execute(text('SET FOREIGN_KEY_CHECKS=0;'))
        connection.execute(text('DROP TABLE IF EXISTS work_preferences;'))
        connection.execute(text('DROP TABLE IF EXISTS study_preferences;'))
        connection.execute(text('DROP TABLE IF EXISTS survey_responses;'))
        connection.execute(text('DROP TABLE IF EXISTS respondents;'))
        connection.execute(text('DROP TABLE IF EXISTS users;'))
        connection.execute(text('SET FOREIGN_KEY_CHECKS=1;'))
        connection.commit()
    
    print("Membuat tabel versi MajorMind Blue...")
    db.create_all()
    
    # Buat ulang admin
    admin = User(name='Admin Veyku', email='admin@veyku.com', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    
    print("Selesai! Database kini sudah punya kolom asal_sekolah, skor_teknik, dll.")
