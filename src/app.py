"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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

#------------------------ RUTAS ------------------------#
# Ruta para obtener usuarios (GET)
@app.route('/user', methods=['GET'])
def get_all_users():
    try:
        all_users = User.query.all()
        return [ user.serialize() for user in all_users ]
    except ValueError as err:
        return {"Message": "An error has occured: " + err}, 500

# Ruta para obtener un usuario por ID (GET)
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return {"Message": "User not found"}, 404
        return user.serialize()
    except ValueError as err:
        return {"Message": "An error has occured: " + err}

# Ruta para obtener planetas (GET)
@app.route('/planet', methods=['GET'])
def get_all_planets():
    try:
        all_planets = Planet.query.all()
        return [ planet.serialize() for planet in all_planets ]
    except ValueError as err:
        return {"Message": "An error has occured: " + err}, 500

# Ruta para obtener un planeta por ID (GET)
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    try:
        planet = Planet.query.get(planet_id)
        if planet is None:
            return {"Message": "Planet not found"}, 404

        return planet.serialize()
    except ValueError as err:
        return {"Message": "An error has occured: " + err}

# Ruta para obtener personajes (GET)
@app.route('/character', methods=['GET'])
def get_all_characters():
    try:
        all_characters = Character.query.all()
        return [ character.serialize() for character in all_characters ]
    except ValueError as err:
        return {"Message": "An error has occured: " + err}, 500

# Ruta para obtener un planeta por ID (GET)
@app.route('/character/<int:character_id>', methods=['GET'])
def get_character_by_id(character_id):

    try:
        character = Character.query.get(character_id)
        if character is None:
            return {"Message": "Character not found"}, 404
        return character.serialize()
    except ValueError as err:
        return {"Message": "An error has occured: " + err}

# Ruta para obtener los favoritos de un usuario por ID (GET)
@app.route('/user/<int:user_id>/favorite', methods=['GET'])
def get_user_favorites(user_id):

    try:
        user = User.query.get(user_id)
        if user is None:
            return {"Message": "User not found"}, 404

        favorites = []
        for favorite in user.favorites:
            if favorite.planet is not None:
                favorites.append(favorite.planet.serialize())
            if favorite.character is not None:
                favorites.append(favorite.character.serialize())

        return jsonify({"favorites": favorites})
    except ValueError as err:
        return {"Message": "An error has occured: " + err}

# Ruta para agregar un planeta como favorito de un usuario por ID (POST)
@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_favorite(user_id, planet_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return {"Message": "User not found"}, 404

        planet = Planet.query.get(planet_id)
        if planet is None:
            return {"Message": "Planet not found"}, 404

        favorite = Favorite(user=user, planet=planet)
        db.session.add(favorite)
        db.session.commit()

        return {"Message": "Planet added to favorites successfully"}, 201
    except ValueError as err:
        return {"Message": "An error has occured: " + err}, 400

# Ruta para agregar un personaje como favorito de un usuario por ID (POST)
@app.route('/user/<int:user_id>/favorite/character/<int:character_id>', methods=['POST'])
def add_character_favorite(user_id, character_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return {"Message": "User not found"}, 404

        character= Character.query.get(character_id)
        if character is None:
            return {"Message": "Character not found"}, 404

        favorite = Favorite(user=user, character=character)
        db.session.add(favorite)
        db.session.commit()

        return {"Message": "Character added to favorites successfully"}, 201
    except ValueError as err:
        return {"Message": "An error has occured: " + err}, 400

# Ruta para eliminar un planeta como favorito de un usuario por ID (DELETE)
@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(user_id, planet_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return {"Message": "User not found"}, 404

        favorite = Favorite.query.filter_by(
            user_id=user_id, planet_id=planet_id
        ).first()
        if favorite is None:
            return {"Message": "Favorite not found"}, 404

        db.session.delete(favorite)
        db.session.commit()

        return {"Message": "Favorite deleted successfully"}, 200
    except ValueError as err:
        return {"Message": "An error has occured: " + err}, 400

# Ruta para eliminar un personaje como favorito de un usuario por ID (DELETE)
@app.route('/user/<int:user_id>/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_character_favorite(user_id, character_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return {"Message": "User not found"}, 404

        favorite = Favorite.query.filter_by(
            user_id=user_id, character_id=character_id
        ).first()
        if favorite is None:
            return {"Message": "Favorite not found"}, 404

        db.session.delete(favorite)
        db.session.commit()

        return {"Message": "Favorite deleted successfully"}, 200
    except ValueError as err:
        return {"Message": "An error has occured: " + err}, 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))