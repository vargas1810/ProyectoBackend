from flask_marshmallow import Marshmallow

ma = Marshmallow()

from .usuario import UsuarioSchema
from .rol import RolSchema
from .ubigeo import UbigeoSchema
from .tipos_test import TiposTestSchema
from .test import TestSchema
from .respuesta import RespuestaSchema
from .condicion import CondicionSchema
from .resultados_preguntas import ResultadosPreguntasSchema
from .resultados import ResultadosSchema
