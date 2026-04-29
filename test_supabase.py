from app import create_app
from models import db
from sqlalchemy import text

app = create_app()

def test_connection():
    with app.app_context():
        try:
            # Mencoba mengeksekusi query sederhana
            db.session.execute(text('SELECT 1'))
            print("=========================================")
            print("✅ BERHASIL! Aplikasi Flask Anda sudah terhubung ke Supabase.")
            print("=========================================")
        except Exception as e:
            print("=========================================")
            print("❌ GAGAL TERHUBUNG!")
            print("Error detail:", e)
            print("=========================================")

if __name__ == '__main__':
    test_connection()
