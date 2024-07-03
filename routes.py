from flask import Blueprint, request, jsonify
import requests
from models import db, Usuario, Rol, Ubigeo, TiposTest, Test, Respuesta, Condicion, ResultadosPreguntas, Resultados
from schemas import UsuarioSchema, RolSchema, UbigeoSchema, TiposTestSchema, TestSchema, RespuestaSchema, CondicionSchema, ResultadosPreguntasSchema, ResultadosSchema, ma

auth = Blueprint('auth', __name__)
usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)
rol_schema = RolSchema()
roles_schema = RolSchema(many=True)
ubigeo_schema = UbigeoSchema()
ubigeos_schema = UbigeoSchema(many=True)
tipos_test_schema = TiposTestSchema()
tipos_tests_schema = TiposTestSchema(many=True)
test_schema = TestSchema()
tests_schema = TestSchema(many=True)
respuesta_schema = RespuestaSchema()
respuestas_schema = RespuestaSchema(many=True)
condicion_schema = CondicionSchema()
condiciones_schema = CondicionSchema(many=True)
resultados_preguntas_schema = ResultadosPreguntasSchema()
resultados_preguntas_schemas = ResultadosPreguntasSchema(many=True)
resultados_schema = ResultadosSchema()
resultados_schemas = ResultadosSchema(many=True)

@auth.route('/register', methods=['POST'])
def register():
    nombre_usuario = request.json.get('nombre_usuario')
    email = request.json.get('email')
    password = request.json.get('password')
    rol_nombre = request.json.get('rol')
    nombre_ciudad = request.json.get('nombre_ciudad')

    rol = Rol.query.filter_by(nombre=rol_nombre).first()
    if not rol:
        return jsonify({'message': 'Invalid role'}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    if Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
        return jsonify({'message': 'Username already exists'}), 400

    ubigeo = Ubigeo.query.filter_by(nombre_ciudad=nombre_ciudad).first()
    if not ubigeo:
        return jsonify({'message': 'Invalid city'}), 400

    new_user = Usuario(
        nombre_usuario=nombre_usuario,
        email=email,
        rol_id=rol.id,
        ubigeo_id=ubigeo.id
    )
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return usuario_schema.jsonify(new_user), 201


def geocode(ciudad):
    api_key = 'TU_API_KEY'  # Cambia esto a tu API key de Google Maps u otro servicio de geocodificación
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={ciudad}&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()['results']
        if results:
            location = results[0]['geometry']['location']
            return location['lat'], location['lng']
    return None, None


@auth.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = Usuario.query.filter_by(email=email).first()

    if user and user.check_password(password):
        return jsonify({
            'authenticated': True,
            'message': 'Login Exitoso',
            'user': usuario_schema.dump(user)
        })
    else:
        return jsonify({
            'authenticated': False,
            'message': 'Credenciales Incorrectas'
        }), 401

@auth.route('/usuarios', methods=['GET'])
def get_usuarios():
    all_users = Usuario.query.all()
    result = usuarios_schema.dump(all_users)
    return jsonify(result)

@auth.route('/roles', methods=['GET'])
def get_roles():
    all_roles = Rol.query.all()
    result = roles_schema.dump(all_roles)
    return jsonify(result)

@auth.route('/ubigeos', methods=['GET'])
def get_ubigeos():
    all_ubigeos = Ubigeo.query.all()
    result = ubigeos_schema.dump(all_ubigeos)
    return jsonify(result)

@auth.route('/tipos_tests', methods=['GET'])
def get_tipos_tests():
    all_tipos_tests = TiposTest.query.all()
    result = tipos_tests_schema.dump(all_tipos_tests)
    return jsonify(result)

@auth.route('/preguntas', methods=['GET'])
def get_preguntas():
    all_preguntas = Test.query.all()
    result = tests_schema.dump(all_preguntas)
    return jsonify(result)

@auth.route('/preguntas/<int:tipo_test_id>', methods=['GET'])
def get_preguntas_por_tipo(tipo_test_id):
    preguntas = Test.query.filter_by(tipo_test_id=tipo_test_id).all()
    result = tests_schema.dump(preguntas)
    return jsonify(result)



@auth.route('/pregunta', methods=['POST'])
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


@auth.route('/respuestas', methods=['GET'])
def get_respuestas():
    all_respuestas = Respuesta.query.all()
    result = respuestas_schema.dump(all_respuestas)
    return jsonify(result)

@auth.route('/respuesta', methods=['POST'])
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


@auth.route('/resultados_preguntas', methods=['POST'])
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


@auth.route('/resultados/<int:estudiante_id>', methods=['GET'])
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


@auth.route('/resultados_estudiante/<int:estudiante_id>', methods=['GET'])
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


@auth.route('/usuario/<int:usuario_id>', methods=['GET'])
def get_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    return usuario_schema.jsonify(usuario)

@auth.route('/ubicaciones', methods=['GET'])
def get_ubicaciones():
    all_ubigeos = Ubigeo.query.all()
    result = ubigeos_schema.dump(all_ubigeos)
    return jsonify(result)

@auth.route('/condicion', methods=['POST'])
def add_condicion():
    nombre_condicion = request.json.get('nombre_condicion')
    min_puntaje = request.json.get('min_puntaje')
    max_puntaje = request.json.get('max_puntaje')
    tipo_test_id = request.json.get('tipo_test_id')

    if not TiposTest.query.get(tipo_test_id):
        return jsonify({'message': 'Invalid tipo_test_id'}), 400

    nueva_condicion = Condicion(
        nombre_condicion=nombre_condicion,
        min_puntaje=min_puntaje,
        max_puntaje=max_puntaje,
        tipo_test_id=tipo_test_id
    )

    db.session.add(nueva_condicion)
    db.session.commit()
    return condicion_schema.jsonify(nueva_condicion), 201

@auth.route('/usuarios/localizacion', methods=['GET'])
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



@auth.route('/usuarios/resultados', methods=['GET'])
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