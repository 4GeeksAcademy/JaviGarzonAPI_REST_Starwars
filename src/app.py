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
from models import db, User, Planet, People, Vehicle, Favorite
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


@app.route('/users', methods=['GET'])
def get_all_users():

    users = User.query.all()

    users_serialized = [user.serialize() for user in users]

    return jsonify({
        "msg": "Users retrieved succesfully",
        "users": users_serialized
    }), 200



# Obtener todos los usuarios:
@app.route('/people', methods=['GET'])
def get_all_people():

    people = People.query.all()

    if not people: 
        return jsonify({
            "msg": "People not found",
        }), 400
    
    people_serialized = [person.serialize() for person in people]

    return jsonify({
        "msg": "People retrieved succesfully",
        "people": people_serialized
    }), 200


# Obtener un usuario:
@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):

    person = People.query.get(people_id)

    if not person: 
        return jsonify({
            "msg": "Person not found",
        }), 404
    
    return jsonify({
        "msg": "Person retrieved succesfully",
        "Person": person.serialize()
    }), 200



# Obtener todos los planetas:
@app.route('/planet', methods=['GET'])
def get_all_planet():

    planets = Planet.query.all()

    if not planets: 
        return jsonify({
            "msg": "Planet not found",
        }), 400
    
    planet_serialized = [planet.serialize() for planet in planets]

    return jsonify({
        "msg": "Planet retrieved succesfully",
        "planet": planet_serialized()
    }), 200


# Obtener un planeta:
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):

    planet = Planet.query.get(planet_id)

    if not planet: 
        return jsonify({
            "msg": "Planet not found",
        }), 404
    return jsonify({
        "msg": "Planet retrieved succesfully",
        "Planet": planet.serialize()
    }), 200


# Obtener todos los Vehiculos:
@app.route('/vehicle', methods=['GET'])
def get_all_vehicle():

    vehicles = Vehicle.query.all()


    if not vehicles: 
        return jsonify({
            "msg": "vehicle not found",
        }), 400
    
    vehicle_serialized = [vehicle.serialize() for vehicle in vehicles]
    
    return jsonify({
            "msg": "vehicle retrieved succesfully",
            "vehicle": vehicle_serialized
        }), 200

# Obtener un Vehiculo:
@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):

    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle: 
        return jsonify({
            "msg": "vehicle not found",
        }), 400
    
    return jsonify({
            "msg": "vehicle retrieved succesfully",
            "vehicle": vehicle.serialize()
        }), 200


# Obtener un usuario:
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):

    user = User.query.get(user_id)

    if not user: 
        return jsonify({
            "msg": "User not found",
        }), 404
    
    return jsonify({
            "msg": "User retrieved succesfully",
            "User": user.serialize()
        }), 200


# Obtener todos favoritos de un usuario:
@app.route('/favorite/<int:user_id>',methods=['GET'])
def get_favorite(user_id):
    
    user = User.query.get(user_id)

    if not user: 
        return jsonify({
            "msg": "User not found",
        }), 400
      
    return jsonify({
        "msg": "User retrieved succesfully",
        "user_id": user.serialize_favorite()
    }), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def create_favorite_planet(planet_id):

    request_data = request.get_json()

    if not request_data or not request_data.get("user_id"):
        return jsonify({"msg" : "Petición incompleta"}), 400

    user = User.query.get(request_data.get("user_id"))
    planet = Planet.query.get(planet_id) 
    if not user:
        return jsonify({"msg" : "El usuario no existe"}), 404
    if not planet:
        return jsonify({"msg" : "El planeta no existe"}), 404
    
    new_favorite = Favorite(
        user_id = user.id, 
        planet_id = planet.id
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({
        "msg" : "Planeta creado con exito",
        "Planeta" : new_favorite.serialize()
    }), 201

#Borrar un planeta de favoritos por id de planeta

@app.route('/favorite/planet/<int:planet_id>', methods = ['DELETE'])
def delete_planet(planet_id):

    request_data = request.get_json()

    if not request_data or not request_data.get("user_id"):
        return jsonify({"msg" : "Petición incompleta"}), 400

    favorite = Favorite.query.filter_by(planet_id = planet_id, user_id = request_data.get("user_id")).first()

    if not favorite:
        return jsonify({"msg" : "Planeta no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Planeta borrado con éxito"}), 200

#Añade una persona a favoritos por id de people

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def create_favorite_people(people_id):

    request_data = request.get_json()

    if not request_data or not request_data.get("user_id"):
        return jsonify({"msg" : "Petición incompleta"}), 400

    user = User.query.get(request_data.get("user_id"))
    person = People.query.get(people_id) 
    if not user:
        return jsonify({"msg" : "El usuario no existe"}), 404
    if not person:
        return jsonify({"msg" : "La persona no existe"}), 404
    
    new_favorite = Favorite(
        user_id = user.id, 
        people_id = person.id
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({
        "msg" : "Persona creado con exito",
        "Persona" : new_favorite.serialize()
    }), 201


#Borrar una persona de favoritos por id de persona


@app.route('/favorite/people/<int:people_id>', methods = ['DELETE'])
def delete_people(people_id):


    request_data = request.get_json()

    if not request_data or not request_data.get("user_id"):
        return jsonify({"msg" : "Petición incompleta"}), 400

    favorite = Favorite.query.filter_by(people_id = people_id, user_id = request_data.get("user_id")).first()

    if not favorite:
        return jsonify({"msg" : "Persona no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Persona borrado con éxito"}), 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
