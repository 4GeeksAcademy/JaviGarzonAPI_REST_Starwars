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


@app.route('/people', methods=['GET'])
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

    people_serialized = [people.serialize() for people in people]

    if not people: 
        return jsonify({
            "msg": "People not found",
        }), 400

    return jsonify({
        "msg": "People retrieved succesfully",
        "people": people_serialized
    }), 200


# Obtener un usuario:
@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):

    people = People.query.get(people_id)

    people_serialized = [people.serialize() for people in people]

    if not people: 
        return jsonify({
            "msg": "Person not found",
        }), 404
    
    return jsonify({
        "msg": "Person retrieved succesfully",
        "Person": people.serialize()
    }), 200



# Obtener todos los planetas:
@app.route('/planet', methods=['GET'])
def get_all_planet():

    planet = Planet.query.all()

    planet_serialized = [planet.serialize() for planet in planet]

    if not planet: 
        return jsonify({
            "msg": "Planet not found",
        }), 400
    return jsonify({
        "msg": "Planet retrieved succesfully",
        "planet": planet_serialized()
    }), 200


# Obtener un planeta:
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):

    planet = Planet.query.get(planet_id)

    planet_serialized = [planet.serialize() for planet in planet]

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

    vehicle = Vehicle.query.all()

    vehicle_serialized = [vehicle.serialize() for vehicle in vehicle]

    if not vehicle: 
        return jsonify({
            "msg": "vehicle not found",
        }), 400
    
    return jsonify({
            "msg": "vehicle retrieved succesfully",
            "vehicle": vehicle.serialized()
        }), 200

# Obtener un Vehiculo:
@app.route('/vehicle', methods=['GET'])
def get_vehicle():

    vehicle = Vehicle.query.get(vehicle.id)

    vehicle_serialized = [vehicle.serialize() for vehicle in vehicle]

    if not vehicle: 
        return jsonify({
            "msg": "vehicle not found",
        }), 400
    
    return jsonify({
            "msg": "vehicle retrieved succesfully",
            "vehicle": vehicle.serialize()
        }), 200

# Obtener todos los usuarios:
@app.route('/user', methods=['GET'])
def get_all_users():

    user = User.query.all()

    planet_serialized = [user.serialize() for user in user]

    if not user: 
        return jsonify({
            "msg": "User not found",
        }), 400

    return jsonify({
            "msg": "User retrieved succesfully",
            "users": user.serialized()
        }), 200


# Obtener un usuario:
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):

    user = User.query.get(user_id)

    user_serialized = [user.serialize() for user in user]

    if not user: 
        return jsonify({
            "msg": "User not found",
        }), 404
    
    return jsonify({
            "msg": "User retrieved succesfully",
            "User": user.serialize()
        }), 200



# Obtener todos favoritos:
@app.route('/favorite/<int:user_id>',methods=['GET'])
def get_favorite(user_id):
    
    user = User.query.get(user_id)

    if not user: 
        return jsonify({
            "msg": "User not found",
        }), 400
      
    return jsonify({
        "msg": "User retrieved succesfully",
        "user_id": user.serialize()
    }), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def create_favorite_planet():

    request_data = request.get_json()

    if not request_data or not request_data.get("planet") or not request_data.get("user"):
        return jsonify({"msg" : "Petición incompleta"}), 400

    user = User.query.get(request_data.get("user_id"))
    planet = Planet.query.get(request_data.get("planet_id")) 
    if not user:
        return jsonify({"msg" : "El usuario no existe"}), 404
    if not planet:
        return jsonify({"msg" : "El planeta no existe"}), 404
    
    new_planet = Planet(
      
        id = request_data.get("id"),
        name = request_data.get("name"),
        description = request_data.get("description"),
        films = request_data.get("films"),
        Affiliations = request_data.get("Afiliations"),
        species= request_data.get("species"),
        places = request_data.get("places"),
        location = request_data.get("location"),
        climate = request_data.get("climate"),
        terrain = request_data.get("terrain"),
        system = request_data.get("system"),
        vehicles = request_data.get("vehicles"),
        weapons = request_data.get("weapons"),
        tool = request_data.get("tool"),
        droids = request_data.get("droids"),
        surface_water = request_data.get("surface_water"),
        
        )

    db.session.add(new_planet)
    db.session.commit()

    return jsonify({
        "msg" : "Planeta creado con exito",
        "Planeta" : new_planet.serialize()
    }), 201


@app.route('/favorite/planet/<int:planet_id>', methods = ['DELETE'])
def delete_planet(planet_id):

    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({"msg" : "Planeta no encontrado"}), 404

    db.session.delete(planet)
    db.session.commit()

    return jsonify({"msg": "Planeta borrado con éxito"}), 200


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def create_favorite_people():

    request_data = request.get_json()

    if not request_data or not request_data.get("people") or not request_data.get("user"):
        return jsonify({"msg" : "Petición incompleta"}), 400

    user = User.query.get(request_data.get("user_id"))
    planet = Planet.query.get(request_data.get("people_id")) 
    if not user:
        return jsonify({"msg" : "El usuario no existe"}), 404
    if not planet:
        return jsonify({"msg" : "La persona no existe"}), 404
    
    new_people = People (
      
                            id = request_data.get("id"),
                            name = request_data.get("name"),
                            gender = request_data.get("gender"),
                            height= request_data.get("height"),
                            species= request_data.get("species"),
                            history = request_data.get("history"),
                            films = request_data.get("films"),
                            Affiliations = request_data.get("Affiliations"),
                            planetlocation = request_data.get("planetlocation"),
                            url = request_data.get("url"),
        
                            )

    db.session.add(new_people)
    db.session.commit()

    return jsonify({
        "msg" : "Persona creado con exito",
        "Persona" : new_people.serialize()
    }), 201


@app.route('/favorite/people/<int:people_id>', methods = ['DELETE'])
def delete_people(people_id):

    people = People.query.get(people_id)

    if not people:
        return jsonify({"msg" : "Persona no encontrado"}), 404

    db.session.delete(people)
    db.session.commit()

    return jsonify({"msg": "Persona borrado con éxito"}), 200







# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
