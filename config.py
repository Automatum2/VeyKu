import os
from dotenv import load_dotenv

# Load file .env jika ada
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'smk1-denpasar-survei-secret-key-2026'
    
    # Deteksi apakah berjalan di server (misal: PythonAnywhere atau Render)
    # Jika ada DATABASE_URL di environment variable, gunakan itu.
    # Jika tidak, gunakan MySQL lokal (XAMPP).
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'mysql+pymysql://root:@localhost/majormind_db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    