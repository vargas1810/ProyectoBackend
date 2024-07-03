from models import ResultadosPreguntas
from . import ma

class ResultadosPreguntasSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ResultadosPreguntas
        load_instance = True
        include_fk = True
