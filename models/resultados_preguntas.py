from . import db

class ResultadosPreguntas(db.Model):
    __tablename__ = 'resultadospreguntas'
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    respuesta_id = db.Column(db.Integer, db.ForeignKey('respuesta.id'), nullable=False)
    tipo_test_id = db.Column(db.Integer, db.ForeignKey('tipos_test.id'), nullable=False)
    estudiante = db.relationship('Usuario', backref=db.backref('resultadospreguntas', lazy=True))
    pregunta = db.relationship('Test', backref=db.backref('resultadospreguntas', lazy=True))
    respuesta = db.relationship('Respuesta', backref=db.backref('resultadospreguntas', lazy=True))
    tipo_test = db.relationship('TiposTest', backref=db.backref('resultadospreguntas', lazy=True))
