import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://proyectosisvita_quix_user:qHhMun2POXm3cIM4LnmTQALrcc5gsgh3@dpg-cpufgclds78s73drp7vg-a.oregon-postgres.render.com/ProyectoSisvita'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
