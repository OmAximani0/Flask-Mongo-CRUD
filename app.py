from flask import Flask, request, jsonify
from os import getenv
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from bson import ObjectId
import json
from utils.encoder import JSONEncoder
from flask_cors import CORS

# load environmets variables from `.env` file
load_dotenv('.env')

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

app.config['MONGO_URI'] = getenv('MONGO_URI')

# Connect to mongo 
mongo_client = MongoClient(app.config.get('MONGO_URI'))
# select the database
db = mongo_client["crud"]
# select collection from database
users = db.user

@app.get('/users')
def list_users():
    response = {}

    try:
        all_users = list(users.find())
    
        # Encode the `ObjectId` of Mongo
        all_users = JSONEncoder().encode(all_users)

        response['users'] = json.loads(all_users)
        response['status'] = 1

        return response, 200
    except Exception as e:
        response['message'] = "Error while operation!"
        response['status'] = 0
        return response, 500
    

@app.get('/users/<string:id>')
def get_user(id):
    response = {}
    try:
        id = ObjectId(id)
        user = users.find_one({'_id': id})
        if user:
            user = JSONEncoder().encode(user)
            response['user'] = json.loads(user)
            response['status'] = 1
            return response, 200
        response['message'] = "User not found!"
        response['status'] = 0
        return response, 404
    except Exception as e:
        response['message'] = "Error while operation!"
        response['status'] = 0
        return response, 500
    

@app.post('/users')
def create_user():
    response = {}

    req_body = request.get_json()
    if req_body:
        name = req_body.get('name')
        email = req_body.get('email') 
        password = req_body.get('password')

        new_user = {
            'name': name,
            'email': email,
            'password': bcrypt.generate_password_hash(password).decode('utf-8')
        }

        try:
            users.insert_one(new_user)
            response['message'] = "User is created!"
            response['status'] = 1
            return jsonify(response), 201
        except Exception as e:
            response['message'] = "Error while creating the user"
            response['status'] = 0
            return jsonify(response), 500

    response['message'] = 'No information provided!'
    response['status'] = 0
    return jsonify(response), 400


@app.put('/users/<string:id>')
def update_user(id):
    response = {}
    try:
        data = request.get_json()
        if data.get('password'):
            response['message'] = "Password can not be updated directly!"
            response['status'] = 0
            return response, 400
        id = ObjectId(id)
        user = users.find_one_and_update({'_id': id}, {"$set": data})
        print(user)
        if user:
            user = JSONEncoder().encode(user)
            response['user'] = "User updated successfully!"
            response['status'] = 1
            return response, 200
        response['message'] = "User not found!"
        response['status'] = 0
        return response, 404
    except Exception as e:
        response['message'] = "Error while operation!"
        response['status'] = 0
        return response, 500

    
@app.delete('/users/<string:id>')
def delete_user(id):
    response = {}
    try:
        id = ObjectId(id)
        user = users.find_one_and_delete({'_id': id})
        if user:
            user = JSONEncoder().encode(user)
            response['message'] = "User deleted successfully!"
            response['status'] = 1
            return response, 200
        response['message'] = "User not found!"
        response['status'] = 0
        return response, 404
    except Exception as e:
        response['message'] = "Error while operation!"
        response['status'] = 0
        return response, 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)