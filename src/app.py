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
from models import db, User, Character, Favorite, Planet, Vehicle
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

#CRUD FOR USERS
#1.READ - query.all()
@app.route('/user', methods=['GET'])
def handle_hello():

    users = User.query.all()
    usuarios_serializados = [persona.serialize() for persona in users]
    return jsonify(usuarios_serializados), 200

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):

    searched_user = User.query.filter_by(id=id).one_or_none()
    usuario_serializado = searched_user.serialize()
    return jsonify(usuario_serializado), 200


#2.CREATE - save()
@app.route('/user', methods = ['POST'])
def add_user():

    body = request.json
    #Llamamos a los elementos del diccionario body
    username = body.get('username', None)
    email = body.get('email', None)
    password = body.get('password', None)

    if username == None or email == None or password == None:
        return jsonify({"msg": "Missing fields"}), 400
    
    try:
        new_user = User(email=email, username=username, password=password)

        db.session.add(new_user) #Memoria RAM
        db.session.commit() #Se guarda con las intruccion SQL CREATE

        return jsonify({"msg": "success"}), 201
    
    except:
        return jsonify({"error" : "Something went wrong!" }), 500

#3.DELETE - delete()
@app.route('/user/<string:username>', methods = ['DELETE'])
def remove_user(username):
    searched_user = User.query.filter_by(username = username).one_or_none()
    
    if searched_user != None:
        db.session.delete(searched_user)
        db.session.commit()
        return jsonify(searched_user.serialize()), 202
    else:
        return jsonify({"error" : f"User with username: {username} not found" }), 500

#4.UPDATE
@app.route('/user/<string:username>', methods = ['PUT'])
def update_user(username):
    searched_user = User.query.filter_by(username = username).one_or_none()
    
    body = request.json
    #Llamamos a los elementos del diccionario body
    new_username = body.get('username',None)
    password = body.get('password', None)

    if searched_user != None:

        if new_username !=None:
            searched_user.username = new_username

        if password !=None:
            searched_user.password = password

        db.session.commit()

        return jsonify(searched_user.serialize()), 202
    else:
        return jsonify({"error" : f"User with username: {username} not found" }), 500


#CRUD FOR FAVORITES
#1.READ
@app.route('/favorites', methods= ['GET'])
def get_favorites():
    favorites = Favorite.query.all()
    fav_serializados = [favorite.serialize() for favorite in favorites]
    return jsonify(fav_serializados), 200
#2.CREATE
@app.route('/favorites', methods=['POST'])
def new_favorite():

    body = request.json
    #Llamamos a los elementos del diccionario body de thunderman
    user_id = body.get('user_id', None)
    character_id = body.get('character_id', None)
    planet_id = body.get('planet_id', None)
    vehicle_id = body.get('vehicle_id', None)

    if character_id == None or user_id ==None or planet_id==None or vehicle_id ==None:
        return jsonify({"error": "Missing user_id or character_id or planet_id or vehicle_id"}), 400
    #Buscar si el usuario, character, planet y vehiculo existen en la tabla
    user = User.query.get(user_id)
    character = Character.query.get(character_id)
    planet = Planet.query.get(planet_id)
    vehicle = Vehicle.query.get(vehicle_id)

    if character == None or user ==None or planet ==None or vehicle ==None:
        return jsonify({"error": f"User with id: {user_id} or Character with id: {character_id} or Planet with id: {planet_id} or Vehicle with id: {vehicle_id} not found "}), 404
    #Creando un favorite
    new_favorite = Favorite(user, character, planet, vehicle)

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()), 200

#DELETE
@app.route('/favorites/<int:id>', methods=['DELETE'])
def remove_favorite(id):
    searched_user = Favorite.query.filter_by(id=id).one_or_none()
    
    if searched_user is not None:
        db.session.delete(searched_user)
        db.session.commit()
        return jsonify(searched_user.serialize()), 202
    else:
        return jsonify({"error": f"Favorite with id: {id} not found"}), 404

#CRUD FOR PLANETS

#1.READ - query.all()
@app.route('/planets', methods=['GET'])
def get_planets():

    planets = Planet.query.all()
    planetas_serializados = [planeta.serialize() for planeta in planets]
    return jsonify(planetas_serializados), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):

    searched_planet = Planet.query.filter_by(id=id).one_or_none()
    planeta_serializado = searched_planet.serialize()
    return jsonify(planeta_serializado), 200

#2.CREATE
@app.route('/planets', methods = ['POST'])
def add_planet():

    body = request.json
    #Llamamos a los elementos del diccionario body
    name = body.get('name', None)
    density = body.get('density', None)
    diameter = body.get('diameter', None)
    orbital_period = body.get('orbital_period', None)
    population = body.get('population', None)
    weater = body.get('weater', None)

    if name == None or density == None or diameter == None or orbital_period == None or population == None or weater == None:
        return jsonify({"msg": "Missing fields"}), 400
    
    try:
        new_planet = Planet(name=name, density=density, diameter = diameter, orbital_period = orbital_period, population= population, weater = weater)

        db.session.add(new_planet) #Memoria RAM
        db.session.commit() #Se guarda con las intruccion SQL CREATE

        return jsonify({"msg": "success"}), 201
    
    except:
        return jsonify({"error" : "Something went wrong! That name has already been used" }), 500

#3.DELETE - delete()
@app.route('/planets/<int:id>', methods = ['DELETE'])
def remove_planets(id):
    searched_planet = Planet.query.get(id)
    if not searched_planet:
        return jsonify({"error": f"Planet with id: {id} not found"}), 404
    
    searched_character = Character.query.filter_by(planet_origin_id=id).first()
    searched_favorite = Favorite.query.filter_by(planet_id=id).first()
    if searched_character or searched_favorite:
        return jsonify({"error": "Cannot delete vehicle. It is added to characters or favorites."}), 400
    else:
        db.session.delete(searched_planet)
        db.session.commit()
        return jsonify(searched_planet.serialize()), 202








#CRUD FOR CHARACTERS
@app.route('/characters', methods=['GET'])
def get_characters():

    characters = Character.query.all()
    personajes_serializados = [personaje.serialize() for personaje in characters]
    return jsonify(personajes_serializados), 200

@app.route('/characters/<int:id>', methods=['GET'])
def get_character(id):

    searched_character = Character.query.filter_by(id=id).one_or_none()
    personaje_serializado = searched_character.serialize()
    return jsonify(personaje_serializado), 200

#2.CREATE
@app.route('/characters', methods = ['POST'])
def add_character():

    body = request.json
    #Llamamos a los elementos del diccionario body
    name = body.get('name', None)
    height = body.get('height', None)
    weight = body.get('weight', None)
    planet_id = body.get('planet_id', None)
    vehicle_id = body.get('vehicle_id', None)
    
    if name == None or height ==None or weight==None or planet_id ==None or vehicle_id ==None:
        return jsonify({"error": "Missing name or height or weight or planet_id or vehicle_id"}), 400
    #Buscar si el planeta y vehiculo existen en la tabla
    planet = Planet.query.get(planet_id)
    vehicle = Vehicle.query.get(vehicle_id)

    if planet == None or vehicle ==None:
        return jsonify({"error": f"Planet with id: {planet_id} or Vehicle with id: {vehicle_id} not found "}), 404
    #Creando un favorite
    new_character = Character(name, height, weight, planet, vehicle)

    db.session.add(new_character)
    db.session.commit()

    return jsonify(new_character.serialize()), 200

#DELETE
@app.route('/characters/<int:id>', methods=['DELETE'])
def remove_character(id):
    searched_character = Character.query.get(id)
    if not searched_character:
        return jsonify({"error": f"Character with id: {id} not found"}), 404
    
    searched_favorite = Favorite.query.filter_by(character_id=id).first()
    if searched_favorite:
        return jsonify({"error": "Cannot delete character. It is added to favorites."}), 400
    else:
        db.session.delete(searched_character)
        db.session.commit()
        return jsonify(searched_character.serialize()), 202


#CRUD FOR VEHICLES
@app.route('/vehicles', methods=['GET'])
def get_vehicles():

    vehicles = Vehicle.query.all()
    vehiculos_serializados = [vehiculo.serialize() for vehiculo in vehicles]
    return jsonify(vehiculos_serializados), 200

@app.route('/vehicles/<int:id>', methods=['GET'])
def get_vehicle(id):
    
    searched_vehicle = Vehicle.query.filter_by(id=id).one_or_none()
    vehiculo_serializado = searched_vehicle.serialize()
    return jsonify(vehiculo_serializado), 200

#2.CREATE
@app.route('/vehicles', methods = ['POST'])
def add_vehicle():

    body = request.json
    #Llamamos a los elementos del diccionario body
    name = body.get('name', None)
    cargo_capacity = body.get('cargo_capacity', None)
    crew = body.get('crew', None)
    model = body.get('model', None)
    passengers = body.get('passengers', None)

    if name == None or cargo_capacity == None or crew == None or model == None or passengers == None:
        return jsonify({"msg": "Missing fields"}), 400
    
    try:
        new_vehicle = Vehicle(name=name, crew=crew, model=model, cargo_capacity=cargo_capacity, passengers=passengers)

        db.session.add(new_vehicle) #Memoria RAM
        db.session.commit() #Se guarda con las intruccion SQL CREATE

        return jsonify({"msg": "success"}), 201
    
    except:
        return jsonify({"error" : "Something went wrong! That name has already been used" }), 500

#3.DELETE - delete()
@app.route('/vehicles/<int:id>', methods = ['DELETE'])
def remove_vehicles(id):
    searched_vehicle = Vehicle.query.get(id)
    if not searched_vehicle:
        return jsonify({"error": f"Vehicle with id: {id} not found"}), 404
    
    searched_character = Character.query.filter_by(vehicle_id=id).first()
    searched_favorite = Favorite.query.filter_by(vehicle_id=id).first()
    if searched_character or searched_favorite:
        return jsonify({"error": "Cannot delete vehicle. It is added to characters or favorites."}), 400
    else:
        db.session.delete(searched_vehicle)
        db.session.commit()
        return jsonify(searched_vehicle.serialize()), 202






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
