from models import Ubigeo
from . import ma

class UbigeoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ubigeo
        load_instance = True
