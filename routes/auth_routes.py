from flask import Blueprint, request, jsonify
from models import db, Usuario, Rol, Ubigeo
from schemas import UsuarioSchema

auth = Blueprint('auth', __name__)

usuario_schema = UsuarioSchema()
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