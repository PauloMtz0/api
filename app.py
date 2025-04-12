from flask import Flask, jsonify
from config import db, migrate
from dotenv import load_dotenv
import os
from routes.user import user_bp
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger
load_dotenv()

app = Flask(__name__)
swagger = Swagger(app)  # Esto debería generar Swagger UI en '/docs'

CORS(app)
app.config['JWT_SECRET_KEY'] = 'Hoy desperte con ganas'
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(user_bp, url_prefix='/users')

# Ruta de prueba para verificar Swagger UI
@app.route('/')
def home():
    return "API funcionando. Accede a /docs para ver la documentación Swagger."

if __name__ == '__main__':
    app.run(debug=True)
