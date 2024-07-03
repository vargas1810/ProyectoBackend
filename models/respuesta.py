from . import db

class Respuesta(db.Model):
    __tablename__ = 'respuesta'
    id = db.Column(db.Integer, primary_key=True)
    nombre_respuesta = db.Column(db.String(255), nullable=False)
    puntaje_respuesta = db.Column(db.Integer, nullable=False)
    tipo_test_id = db.Column(db.Integer, db.ForeignKey('tipos_test.id'), nullable=False)
    tipo_test = db.relationship('TiposTest', backref=db.backref('respuestas', lazy=True))
