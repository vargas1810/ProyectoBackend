from . import db
from werkzeug.security import generate_password_hash, check_password_hash

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
