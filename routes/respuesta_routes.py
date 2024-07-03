from flask import Blueprint, request, jsonify
from models import Respuesta
from schemas import RespuestaSchema
from models import db

respuesta_bp = Blueprint('respuesta', __name__)

respuesta_schema = RespuestaSchema()
respuestas_schema = RespuestaSchema(many=True)

@respuesta_bp.route('/respuestas', methods=['GET'])
def get_respuestas():
    all_respuestas = Respuesta.query.all()
    result = respuestas_schema.dump(all_respuestas)
    return jsonify(result)

@respuesta_bp.route('/respuesta', methods=['POST'])
def add_respuesta():
    nombre_respuesta = request.json['nombre_respuesta']
    puntaje_respuesta = request.json['puntaje_respuesta']
    tipo_test_id = request.json['tipo_test_id']

    if Respuesta.query.filter_by(nombre_respuesta=nombre_respuesta, tipo_test_id=tipo_test_id).first():
        return jsonify({'message': 'Respuesta already exists for this test'}), 400
    
    new_respuesta = Respuesta(
        nombre_respuesta=nombre_respuesta,
        puntaje_respuesta=puntaje_respuesta,
        tipo_test_id=tipo_test_id
    )
    db.session.add(new_respuesta)
    db.session.commit()
    return respuesta_schema.jsonify(new_respuesta), 201