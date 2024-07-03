from flask import Blueprint, request, jsonify
from models import Test
from schemas import TestSchema
from models import db

test_bp = Blueprint('test', __name__)

test_schema = TestSchema()
tests_schema = TestSchema(many=True)

@test_bp.route('/preguntas', methods=['GET'])
def get_preguntas():
    all_preguntas = Test.query.all()
    result = tests_schema.dump(all_preguntas)
    return jsonify(result)


@test_bp.route('/preguntas/<int:tipo_test_id>', methods=['GET'])
def get_preguntas_por_tipo(tipo_test_id):
    preguntas = Test.query.filter_by(tipo_test_id=tipo_test_id).all()
    result = tests_schema.dump(preguntas)
    return jsonify(result)



@test_bp.route('/pregunta', methods=['POST'])
def add_pregunta():
    nombre_pregunta = request.json['nombre_pregunta']
    tipo_test_id = request.json['tipo_test_id']

    if Test.query.filter_by(nombre_pregunta=nombre_pregunta).first():
        return jsonify({'message': 'Pregunta already exists'}), 400

    new_pregunta = Test(
        nombre_pregunta=nombre_pregunta,
        tipo_test_id=tipo_test_id
    )
    db.session.add(new_pregunta)
    db.session.commit()
    return test_schema.jsonify(new_pregunta), 201

