from flask import Flask
from flask_cors import CORS
from __init__ import create_app

app = create_app()

# Configurar CORS para permitir solicitudes desde cualquier origen
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
