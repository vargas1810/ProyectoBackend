from flask import Blueprint, jsonify
from models import Condicion
from schemas import CondicionSchema

condicion_bp = Blueprint('condicion', __name__)

condicion_schema = CondicionSchema()
condiciones_schema = CondicionSchema(many=True)

@condicion_bp.route('/condiciones', methods=['GET'])
def get_condiciones():
    all_condiciones = Condicion.query.all()
    result = condiciones_schema.dump(all_condiciones)
    return jsonify(result)
    