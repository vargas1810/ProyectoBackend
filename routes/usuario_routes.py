from flask import Blueprint, jsonify
from models import Usuario
from models.condicion import Condicion
from models.resultados import Resultados
from models.resultados_preguntas import ResultadosPreguntas
from models.tipos_test import TiposTest
from models.ubigeo import Ubigeo
from schemas import UsuarioSchema

usuario_bp = Blueprint('usuario', __name__)

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

@usuario_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    all_users = Usuario.query.all()
    result = usuarios_schema.dump(all_users)
    return jsonify(result)

@usuario_bp.route('/usuario/<int:usuario_id>', methods=['GET'])
def get_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    return usuario_schema.jsonify(usuario)

@usuario_bp.route('/usuarios/localizacion', methods=['GET'])
def get_usuarios_localizacion():
    usuarios = Usuario.query.all()
    usuarios_localizacion = []

    for usuario in usuarios:
        ubigeo = Ubigeo.query.get(usuario.ubigeo_id)
        if ubigeo and ubigeo.latitud and ubigeo.longitud:
            resultado_test_1 = Resultados.query.filter_by(estudiante_id=usuario.id, tipo_test_id=1).first()
            resultado_test_2 = Resultados.query.filter_by(estudiante_id=usuario.id, tipo_test_id=2).first()

            color_test_1 = 'gray'
            color_test_2 = 'gray'

            if resultado_test_1:
                condicion_test_1 = Condicion.query.get(resultado_test_1.condicion_id)
                if condicion_test_1:
                    color_test_1 = condicion_test_1.color

            if resultado_test_2:
                condicion_test_2 = Condicion.query.get(resultado_test_2.condicion_id)
                if condicion_test_2:
                    color_test_2 = condicion_test_2.color

            usuario_info = {
                'nombre_usuario': usuario.nombre_usuario,
                'email': usuario.email,
                'ciudad': ubigeo.nombre_ciudad,
                'latitud': ubigeo.latitud,
                'longitud': ubigeo.longitud,
                'color_test_1': color_test_1,
                'color_test_2': color_test_2
            }
            usuarios_localizacion.append(usuario_info)

    return jsonify(usuarios_localizacion), 200




@usuario_bp.route('/usuarios/resultados', methods=['GET'])
def get_usuarios_resultados():
    usuarios = Usuario.query.all()
    usuarios_resultados = []

    for usuario in usuarios:
        resultado_test_1 = Resultados.query.filter_by(estudiante_id=usuario.id, tipo_test_id=1).first()
        resultado_test_2 = Resultados.query.filter_by(estudiante_id=usuario.id, tipo_test_id=2).first()

        color_test_1 = 'gray'
        nombre_tipo_test_1 = None
        if resultado_test_1:
            condicion_test_1 = Condicion.query.get(resultado_test_1.condicion_id)
            tipo_test_1 = TiposTest.query.get(1)
            if condicion_test_1 and tipo_test_1:
                color_test_1 = condicion_test_1.color
                nombre_tipo_test_1 = tipo_test_1.nombre_tipo

        color_test_2 = 'gray'
        nombre_tipo_test_2 = None
        if resultado_test_2:
            condicion_test_2 = Condicion.query.get(resultado_test_2.condicion_id)
            tipo_test_2 = TiposTest.query.get(2)
            if condicion_test_2 and tipo_test_2:
                color_test_2 = condicion_test_2.color
                nombre_tipo_test_2 = tipo_test_2.nombre_tipo

        # Filtrar los usuarios solo si ambos colores son grises
        if not (color_test_1 == 'gray' and color_test_2 == 'gray'):
            usuario_info = {
                'nombre_usuario': usuario.nombre_usuario,
                'email': usuario.email,
                'ciudad': usuario.ubigeo.nombre_ciudad,
                'color_test_1': color_test_1,
                'nombre_tipo_test_1': nombre_tipo_test_1,
                'color_test_2': color_test_2,
                'nombre_tipo_test_2': nombre_tipo_test_2
            }
            usuarios_resultados.append(usuario_info)

    return jsonify(usuarios_resultados), 200



@usuario_bp.route('/informacion', methods=['GET'])
def get_informacion_completa():
    usuarios = Usuario.query.all()
    informacion_completa = []

    for usuario in usuarios:
        ubigeo = Ubigeo.query.get(usuario.ubigeo_id)
        resultado_test_1 = Resultados.query.filter_by(estudiante_id=usuario.id, tipo_test_id=1).first()
        resultado_test_2 = Resultados.query.filter_by(estudiante_id=usuario.id, tipo_test_id=2).first()

        color_test_1 = 'gray'
        condicion_test_1 = 'N/A'
        puntaje_test_1 = 'N/A'

        if resultado_test_1:
            condicion_obj_1 = Condicion.query.get(resultado_test_1.condicion_id)
            if condicion_obj_1:
                color_test_1 = condicion_obj_1.color
                condicion_test_1 = condicion_obj_1.nombre_condicion
                puntaje_test_1 = sum([rp.respuesta.puntaje_respuesta for rp in ResultadosPreguntas.query.filter_by(estudiante_id=usuario.id, tipo_test_id=1).all()])

        color_test_2 = 'gray'
        condicion_test_2 = 'N/A'
        puntaje_test_2 = 'N/A'

        if resultado_test_2:
            condicion_obj_2 = Condicion.query.get(resultado_test_2.condicion_id)
            if condicion_obj_2:
                color_test_2 = condicion_obj_2.color
                condicion_test_2 = condicion_obj_2.nombre_condicion
                puntaje_test_2 = sum([rp.respuesta.puntaje_respuesta for rp in ResultadosPreguntas.query.filter_by(estudiante_id=usuario.id, tipo_test_id=2).all()])

        usuario_info = {
            'nombre_usuario': usuario.nombre_usuario,
            'email': usuario.email,
            'ciudad': ubigeo.nombre_ciudad if ubigeo else 'N/A',
            'latitud': ubigeo.latitud if ubigeo else 'N/A',
            'longitud': ubigeo.longitud if ubigeo else 'N/A',
            'color_test_1': color_test_1,
            'condicion_test_1': condicion_test_1,
            'puntaje_test_1': puntaje_test_1,
            'color_test_2': color_test_2,
            'condicion_test_2': condicion_test_2,
            'puntaje_test_2': puntaje_test_2,
        }
        informacion_completa.append(usuario_info)

    return jsonify(informacion_completa), 200

