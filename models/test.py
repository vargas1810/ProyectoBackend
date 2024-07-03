from . import db

class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    nombre_pregunta = db.Column(db.String(255), nullable=False)
    tipo_test_id = db.Column(db.Integer, db.ForeignKey('tipos_test.id'), nullable=False)
    tipo_test = db.relationship('TiposTest', backref=db.backref('test', lazy=True))
