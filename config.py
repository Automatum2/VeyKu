import os
from dotenv import load_dotenv

# Load file .env jika ada
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'smk1-denpasar-survei-secret-key-2026'
    
    db_url = os.environ.get('DATABASE_URL')
    # Supabase kadang menggunakan 'postgres://', sedangkan SQLAlchemy butuh 'postgresql://'
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    if not db_url:
        raise ValueError("DATABASE_URL tidak ditemukan di .env. Pastikan Anda telah mengatur URL koneksi Supabase.")
        
    SQLALCHEMY_DATABASE_URI = db_url
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
