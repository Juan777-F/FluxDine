import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'pikda-secret-dev-2024')

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:Root2025!@127.0.0.1:3308/la_pikda_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_ENABLED = True


    