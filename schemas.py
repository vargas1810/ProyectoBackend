from flask_marshmallow import Marshmallow
from models import Usuario, Rol, Ubigeo, TiposTest, Test, Respuesta, Condicion, ResultadosPreguntas, Resultados

ma = Marshmallow()

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        include_fk = True

class RolSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rol
        load_instance = True

class UbigeoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ubigeo
        load_instance = True

class TiposTestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TiposTest
        load_instance = True

class TestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Test
        load_instance = True
        include_fk = True

class RespuestaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Respuesta
        load_instance = True
        include_fk = True


class CondicionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Condicion
        load_instance = True
    color = ma.String()


class ResultadosPreguntasSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ResultadosPreguntas
        load_instance = True
        include_fk = True

class ResultadosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Resultados
        load_instance = True
        include_fk = True
