from flask import Blueprint, jsonify
from models import Ubigeo
from schemas import UbigeoSchema

ubicacion_bp = Blueprint('ubicacion', __name__)

ubigeo_schema = UbigeoSchema()
ubigeos_schema = UbigeoSchema(many=True)

@ubicacion_bp.route('/ubigeos', methods=['GET'])
def get_ubigeos():
    all_ubigeos = Ubigeo.query.all()
    result = ubigeos_schema.dump(all_ubigeos)
    return jsonify(result)
