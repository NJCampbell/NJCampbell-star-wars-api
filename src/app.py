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


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# GET people/planets/vehicles ALL


@app.route('/characters', methods=['GET'])
def get_people():
    json_text = jsonify(people)
    return json_text


@app.route('/planets', methods=['GET'])
def get_planets():
    json_text = jsonify(planets)
    return json_text


@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    json_text = jsonify(vehicles)
    return json_text

# GET users/user favorites


@app.route('/users', methods=['GET'])
def get_users():
    json_text = jsonify(users)
    return json_text


@app.route('/users/favorites', methods=['GET'])
def get_vehicles():
    json_text = jsonify(user_favorites)
    return json_text

# GET individual person/planet


@app.route('/characters/uid', methods=['GET'])
def get_people():
    json_text = jsonify(people)
    return json_text


@app.route('/planets/uid', methods=['GET'])
def get_planets():
    json_text = jsonify(planets)
    return json_text

# POST favorites/fave planet / fave people


@app.route('/favorite/planet/uid', methods=['POST'])
def add_fave_planet():
    request_body = request.get_json(force=True)
    print("Incoming request with the following body", request_body)
    fave_planet.append(request_body)
    return jsonify(fave_planet)


@app.route('/favorite/character', methods=['POST'])
def add_fave_person():
    request_body = request.get_json(force=True)
    print("Incoming request with the following body", request_body)
    fave_person.append(request_body)
    return jsonify(fave_person)

# DELETE favorites planet/people


@app.route('/favorite/planet/uid', methods=['DELETE'])
def delete_fave_planet(position):
    print("This is the position to delete: ", position)
    del planets[position]
    return jsonify(planets)


@app.route('/favorite/character/uid', methods=['DELETE'])
def delete_fave_person(position):
    print("This is the position to delete: ", position)
    del characters[position]
    return jsonify(characters)


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
