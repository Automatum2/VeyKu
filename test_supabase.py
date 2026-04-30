import sys
import os

# Tambahkan direktori saat ini ke path agar bisa import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db
from sqlalchemy import text

app = create_app()

def test_connection():
    print("=" * 40)
    print("Mengecek Koneksi ke Supabase...")
    print("=" * 40)
    
    with app.app_context():
        try:
            # Mencoba mengeksekusi query sederhana
            result = db.session.execute(text('SELECT NOW();'))
            current_time = result.scalar()
            
            print("SUCCESS: BERHASIL TERHUBUNG!")
            print(f"Waktu Server Database: {current_time}")
            print("-" * 40)
            print("Konfigurasi Database:")
            print(f"URI: {app.config['SQLALCHEMY_DATABASE_URI'].split('@')[-1]}") # Sembunyikan password
            print("=" * 40)
            
        except Exception as e:
            print("FAILED: GAGAL TERHUBUNG!")
            print(f"Error detail: {str(e)}")
            print("=" * 40)

if __name__ == "__main__":
    test_connection()
