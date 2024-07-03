from . import db

class Ubigeo(db.Model):
    __tablename__ = 'ubigeo'
    id = db.Column(db.Integer, primary_key=True)
    nombre_ciudad = db.Column(db.String(255), nullable=False)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
