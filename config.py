import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:vargas1810@localhost/ProyectoSisvitaMax2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
