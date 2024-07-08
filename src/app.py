"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from .utils import APIException, generate_sitemap
from .admin import setup_admin
from .models import db, Usuario, Planeta, Personaje, Favorito
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///starwars.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people():
    
    personajes = Personaje.query.all()
    return jsonify([personaje.serialize() for personaje in personajes]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    
    personaje = Personaje.query.get_or_404(people_id)
    return jsonify(personaje.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():

    planetas = Planeta.query.all()
    return jsonify([planeta.serialize() for planeta in planetas]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planeta = Planeta.query.get_or_404(planet_id)
    return jsonify(planeta.serialize()), 200

@app.route('/users', methods=['GET'])
def get_users():
    usuarios = Usuario.query.all()
    return jsonify([usuario.serialize() for usuario in usuarios]), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    usuario_id = request.args.get('user_id')
    usuario = Usuario.query.get_or_404(usuario_id)
    return jsonify([favorito.serialize() for favorito in usuario.favoritos]), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    usuario_id = request.json.get('user_id')
    favorito = Favorito(usuario_id=usuario_id, planeta_id=planet_id)
    db.session.add(favorito)
    db.session.commit()
    return jsonify({"message": "Planeta favorito agregado"}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    usuario_id = request.json.get('user_id')
    favorito = Favorito(usuario_id=usuario_id, personaje_id=people_id)
    db.session.add(favorito)
    db.session.commit()
    return jsonify({"message": "Personaje favorito agregado"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    usuario_id = request.json.get('user_id')
    favorito = Favorito.query.filter_by(usuario_id=usuario_id, planeta_id=planet_id).first_or_404()
    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"message": "Planeta favorito eliminado"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    usuario_id = request.json.get('user_id')
    favorito = Favorito.query.filter_by(usuario_id=usuario_id, personaje_id=people_id).first_or_404()
    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"message": "Personaje favorito eliminado"}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
