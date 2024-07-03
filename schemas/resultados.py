from models import Resultados
from . import ma

class ResultadosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Resultados
        load_instance = True
        include_fk = True
