from flask import Blueprint, jsonify
from models import TiposTest
from schemas import TiposTestSchema

tipos_test_bp = Blueprint('tipos_test', __name__)

tipos_test_schema = TiposTestSchema()
tipos_tests_schema = TiposTestSchema(many=True)

@tipos_test_bp.route('/tipos_tests', methods=['GET'])
def get_tipos_tests():
    all_tipos_tests = TiposTest.query.all()
    result = tipos_tests_schema.dump(all_tipos_tests)
    return jsonify(result)


