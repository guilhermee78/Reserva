import os

class Config:
    HOST = '0.0.0.0'
    PORT = 5002
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///reservas.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False