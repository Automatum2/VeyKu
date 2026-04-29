from app import create_app
from models import db
from models.user import User
import sys

app = create_app()

def init_db():
    with app.app_context():
        # Buat semua tabel
        print("Mulai membuat tabel di database...")
        db.create_all()
        print("Tabel berhasil dibuat!")

        # Cek apakah admin sudah ada
        admin = User.query.filter_by(email='jayajeje63@gmail.com').first()
        if not admin:
            print("Membuat akun admin default...")
            admin = User(name='AdminJMK', email='[EMAIL_ADDRESS]', role='admin')
            admin.set_password('543643')
            db.session.add(admin)
            db.session.commit()
            print("Akun admin berhasil dibuat!")
            print("Email: [EMAIL_ADDRESS]")
            print("Password: 543643")
        else:
            print("Akun admin sudah ada di database.")

if __name__ == '__main__':
    init_db()
