from models import Respuesta
from . import ma

class RespuestaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Respuesta
        load_instance = True
        include_fk = True
