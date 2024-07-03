from flask import Blueprint, request, jsonify
from models import ResultadosPreguntas, Resultados, Condicion, TiposTest, Usuario
from schemas import ResultadosPreguntasSchema, ResultadosSchema
from models import db

resultados_bp = Blueprint('resultados', __name__)

resultados_preguntas_schema = ResultadosPreguntasSchema()
resultados_schema = ResultadosSchema()
resultados_schemas = ResultadosSchema(many=True)

@resultados_bp.route('/resultados_preguntas', methods=['POST'])
def add_resultado_pregunta():
    estudiante_id = request.json['estudiante_id']
    pregunta_id = request.json['pregunta_id']
    respuesta_id = request.json['respuesta_id']
    tipo_test_id = request.json['tipo_test_id']

    if ResultadosPreguntas.query.filter_by(estudiante_id=estudiante_id, pregunta_id=pregunta_id, tipo_test_id=tipo_test_id).first():
        return jsonify({'message': 'Pregunta already answered by this student'}), 400

    new_resultado_pregunta = ResultadosPreguntas(
        estudiante_id=estudiante_id,
        pregunta_id=pregunta_id,
        respuesta_id=respuesta_id,
        tipo_test_id=tipo_test_id
    )
    db.session.add(new_resultado_pregunta)
    db.session.commit()
    return resultados_preguntas_schema.jsonify(new_resultado_pregunta), 201

@resultados_bp.route('/resultados/<int:estudiante_id>', methods=['GET'])
def get_resultados(estudiante_id):
    tipo_test_id = request.args.get('tipo_test_id', type=int)

    if not tipo_test_id:
        return jsonify({'message': 'El tipo de test es requerido'}), 400

    resultados_preguntas = ResultadosPreguntas.query.filter_by(estudiante_id=estudiante_id, tipo_test_id=tipo_test_id).all()
    if not resultados_preguntas:
        return jsonify({'message': 'No hay resultados para este estudiante y tipo de test'}), 404
    
    total_puntaje = sum([respuesta.respuesta.puntaje_respuesta for respuesta in resultados_preguntas])
    
    condicion = Condicion.query.filter(
        Condicion.min_puntaje <= total_puntaje,
        Condicion.max_puntaje >= total_puntaje,
        Condicion.tipo_test_id == tipo_test_id
    ).first()
    
    if not condicion:
        return jsonify({'message': 'No condition found for this score'}), 404

    if Resultados.query.filter_by(estudiante_id=estudiante_id, tipo_test_id=tipo_test_id).first():
        return jsonify({'message': 'Ya existe un resultado para este test'}), 400

    new_resultado = Resultados(
        estudiante_id=estudiante_id,
        condicion_id=condicion.id,
        tipo_test_id=tipo_test_id
    )
    
    db.session.add(new_resultado)
    db.session.commit()

    return jsonify({
        'estudiante_id': estudiante_id,
        'condicion_id': condicion.id,
        'condicion': condicion.nombre_condicion,
        'color': condicion.color
    }), 201

@resultados_bp.route('/resultados_estudiante/<int:estudiante_id>', methods=['GET'])
def get_resultados_estudiante(estudiante_id):
    resultados = Resultados.query.filter_by(estudiante_id=estudiante_id).all()
    if not resultados:
        return jsonify({'message': 'No hay resultados para este estudiante'}), 404

    resultados_extendidos = []
    for resultado in resultados:
        tipo_test = TiposTest.query.get(resultado.tipo_test_id)
        condicion = Condicion.query.get(resultado.condicion_id)

        resultado_extendido = {
            'estudiante_id': resultado.estudiante_id,
            'tipo_test_id': resultado.tipo_test_id,
            'nombre_tipo_test': tipo_test.nombre_tipo,
            'condicion_id': resultado.condicion_id,
            'nombre_condicion': condicion.nombre_condicion
        }
        resultados_extendidos.append(resultado_extendido)
    
    return jsonify(resultados_extendidos), 200