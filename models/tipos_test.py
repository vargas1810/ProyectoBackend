from . import db

class TiposTest(db.Model):
    __tablename__ = 'tipos_test'
    id = db.Column(db.Integer, primary_key=True)
    nombre_tipo = db.Column(db.String(255), nullable=False)
