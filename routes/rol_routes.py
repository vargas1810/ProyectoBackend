from flask import Blueprint, jsonify
from models import Rol
from schemas import RolSchema

rol_bp = Blueprint('rol', __name__)

rol_schema = RolSchema()
roles_schema = RolSchema(many=True)

@rol_bp.route('/roles', methods=['GET'])
def get_roles():
    all_roles = Rol.query.all()
    result = roles_schema.dump(all_roles)
    return jsonify(result)

