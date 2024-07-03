from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .usuario import Usuario
from .rol import Rol
from .ubigeo import Ubigeo
from .tipos_test import TiposTest
from .test import Test
from .respuesta import Respuesta
from .condicion import Condicion
from .resultados_preguntas import ResultadosPreguntas
from .resultados import Resultados
