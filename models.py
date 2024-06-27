from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

class Ubigeo(db.Model):
    __tablename__ = 'ubigeo'
    id = db.Column(db.Integer, primary_key=True)
    nombre_ciudad = db.Column(db.String(255), nullable=False)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    ubigeo_id = db.Column(db.Integer, db.ForeignKey('ubigeo.id'), nullable=False)
    rol = db.relationship('Rol', backref=db.backref('usuarios', lazy=True))
    ubigeo = db.relationship('Ubigeo', backref=db.backref('usuarios', lazy=True))

    def set_password(self, password):
        self.contrasena = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contrasena, password)

class TiposTest(db.Model):
    __tablename__ = 'tipos_test'
    id = db.Column(db.Integer, primary_key=True)
    nombre_tipo = db.Column(db.String(255), nullable=False)

class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    nombre_pregunta = db.Column(db.String(255), nullable=False)
    tipo_test_id = db.Column(db.Integer, db.ForeignKey('tipos_test.id'), nullable=False)
    tipo_test = db.relationship('TiposTest', backref=db.backref('test', lazy=True))

class Respuesta(db.Model):
    __tablename__ = 'respuesta'
    id = db.Column(db.Integer, primary_key=True)
    nombre_respuesta = db.Column(db.String(255), nullable=False)
    puntaje_respuesta = db.Column(db.Integer, nullable=False)
    tipo_test_id = db.Column(db.Integer, db.ForeignKey('tipos_test.id'), nullable=False)
    tipo_test = db.relationship('TiposTest', backref=db.backref('respuestas', lazy=True))


class Condicion(db.Model):
    __tablename__ = 'condicion'
    id = db.Column(db.Integer, primary_key=True)
    nombre_condicion = db.Column(db.String(255), nullable=False)
    min_puntaje = db.Column(db.Integer, nullable=False)
    max_puntaje = db.Column(db.Integer, nullable=False)
    tipo_test_id = db.Column(db.Integer, db.ForeignKey('tipos_test.id'), nullable=False)
    tipo_test = db.relationship('TiposTest', backref=db.backref('condiciones', lazy=True))


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

class Resultados(db.Model):
    __tablename__ = 'resultados'
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    condicion_id = db.Column(db.Integer, db.ForeignKey('condicion.id'), nullable=False)
    tipo_test_id = db.Column(db.Integer, db.ForeignKey('tipos_test.id'), nullable=False)
    estudiante = db.relationship('Usuario', backref=db.backref('resultados', lazy=True))
    condicion = db.relationship('Condicion', backref=db.backref('resultados', lazy=True))
    tipo_test = db.relationship('TiposTest', backref=db.backref('resultados', lazy=True))
