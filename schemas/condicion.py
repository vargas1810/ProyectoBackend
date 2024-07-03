from models import Condicion
from . import ma

class CondicionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Condicion
        load_instance = True
        include_fk = True
