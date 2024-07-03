from . import db

class Resultados(db.Model):
    __tablename__ = 'resultados'
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    condicion_id = db.Column(db.Integer, db.ForeignKey('condicion.id'), nullable=False)
    tipo_test_id = db.Column(db.Integer, db.ForeignKey('tipos_test.id'), nullable=False)
    estudiante = db.relationship('Usuario', backref=db.backref('resultados', lazy=True))
    condicion = db.relationship('Condicion', backref=db.backref('resultados', lazy=True))
    tipo_test = db.relationship('TiposTest', backref=db.backref('resultados', lazy=True))
