from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from schemas import ma
from routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    ma.init_app(app)

    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app
