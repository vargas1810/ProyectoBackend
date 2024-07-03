from models import TiposTest
from . import ma

class TiposTestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TiposTest
        load_instance = True
