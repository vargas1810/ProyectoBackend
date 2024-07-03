from flask import Blueprint

from .auth_routes import auth as auth_blueprint
from .usuario_routes import usuario_bp as usuario_blueprint
from .rol_routes import rol_bp as rol_blueprint
from .ubicacion_routes import ubicacion_bp as ubicacion_blueprint
from .tipos_test_routes import tipos_test_bp as tipos_test_blueprint
from .test_routes import test_bp as test_blueprint
from .respuesta_routes import respuesta_bp as respuesta_blueprint
from .resultados_routes import resultados_bp as resultados_blueprint
from .condicion_routes import condicion_bp as condicion_blueprint


def register_blueprints(app):
    app.register_blueprint(auth_blueprint, url_prefix='/api')
    app.register_blueprint(usuario_blueprint, url_prefix='/api')
    app.register_blueprint(rol_blueprint, url_prefix='/api')
    app.register_blueprint(ubicacion_blueprint, url_prefix='/api')
    app.register_blueprint(tipos_test_blueprint, url_prefix='/api')
    app.register_blueprint(test_blueprint, url_prefix='/api')
    app.register_blueprint(respuesta_blueprint, url_prefix='/api')
    app.register_blueprint(resultados_blueprint, url_prefix='/api')
    app.register_blueprint(condicion_blueprint, url_prefix='/api')
    
__all__ = ['register_blueprints']
