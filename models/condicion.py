from . import db

class Condicion(db.Model):
    __tablename__ = 'condicion'
    id = db.Column(db.Integer, primary_key=True)
    nombre_condicion = db.Column(db.String(100), nullable=False)
    min_puntaje = db.Column(db.Integer, nullable=False)
    max_puntaje = db.Column(db.Integer, nullable=False)
    tipo_test_id = db.Column(db.Integer, db.ForeignKey('tipos_test.id'), nullable=False)
    color = db.Column(db.String(7), nullable=False)  # Nuevo campo para el color
