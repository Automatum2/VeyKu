import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'smk1-denpasar-survei-secret-key-2026'
    
    # Konfigurasi MySQL (XAMPP)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:@localhost/majormind_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
