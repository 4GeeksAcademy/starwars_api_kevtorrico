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
from models import db, User
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


#READ - query.all()
@app.route('/user', methods=['GET'])
def handle_hello():

    users = User.query.all()
    usuarios_serializados = [persona.serialize() for persona in users]
    return jsonify(usuarios_serializados), 200


#CREATE - save()
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


#DELETE - delete()

@app.route('/user/<string:username>', methods = ['DELETE'])
def remove_user(username):
    searched_user = User.query.filter_by(username = username).one_or_none()
    
    if searched_user != None:
        db.session.delete(searched_user)
        db.session.commit()
        return jsonify(searched_user.serialize()), 202
    else:
        return jsonify({"error" : f"User with username: {username} not found" }), 500




#CREATE - UPDATE
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
















# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
