from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(12), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __init__(self, email, password, username):
        self.email = email
        self.password = password
        self.username = username
        self.is_active = True

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
            "username": self.username
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(42), unique=True, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    planet_origin_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=False)
    planet = db.relationship("Planet")
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id"), nullable=False)
    vehicle = db.relationship("Vehicle")

    def __init__(self, name, height, weight, planet, vehicle):
        self.name = name
        self.height = height
        self.weight = weight
        self.planet = planet
        self.vehicle = vehicle


    def serialize(self):
        return {
            "name" : self.name,
            "height" : self.height,
            "weight" : self.weight,
            "planet" : self.planet_origin_id,
            "vehicle" : self.vehicle_id
        }


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(42), unique=True, nullable=False)
    density = db.Column(db.Float, nullable=False)
    diameter = db.Column(db.Float, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    weater = db.Column(db.String(42), nullable= False)

    def __init__(self, name, density, diameter, orbital_period, population, weater):
        self.name = name
        self.density = density
        self.diameter = diameter
        self.orbital_period = orbital_period
        self.population = population
        self.weater = weater

    def serialize(self):
        return {
            "name" : self.name,
            "density" : self.density,
            "diameter" : self.diameter,
            "orbital_period" : self.orbital_period,
            "population" : self.population,
            "weater" : self.weater
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(42), unique=True, nullable=False)
    crew = db.Column(db.Integer, nullable=False)
    model = db.Column(db.String(15), nullable=False)
    cargo_capacity = db.Column(db.Float, nullable=False)
    passengers = db.Column(db.Integer, nullable=False)

    def __init__(self, name, crew, model, cargo_capacity, passengers):
        self.name = name
        self.crew = crew
        self.model = model
        self.cargo_capacity = cargo_capacity
        self.passengers = passengers
   
    def serialize(self):
        return {
            "name" : self.name,
            "crew" : self.crew,
            "model" : self.model,
            "cargo_capacity" : self.cargo_capacity,
            "passengers" : self.passengers
        }


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    user = db.relationship("User") #Objeto de python

    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable = False)
    character = db.relationship("Character")

    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable = False)
    planet = db.relationship("Planet")

    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id"), nullable = False)
    vehicle = db.relationship("Vehicle")

    #Cuando es una relacion, se construye a partir del objeto
    def __init__(self, user, character, planet, vehicle):
        self.user = user
        self.character = character
        self.planet = planet
        self.vehicle = vehicle

    def serialize(self):
        return {
            "id" : self.id,
            "user": self.user_id,
            "character" : self.character_id,
            "planet" : self.planet_id,
            "vehicle": self.vehicle_id
        }
