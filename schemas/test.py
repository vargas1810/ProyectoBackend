from models import Test
from . import ma

class TestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Test
        load_instance = True
        include_fk = True
