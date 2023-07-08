from models.user import User
from mongoengine.errors import DoesNotExist
import json
from flask import request, Blueprint
from app import app
from flask_bcrypt import Bcrypt

users_blueprint = Blueprint('users', __name__)

@users_blueprint.get('/users')
def list_users():
    response = {}
    try:
        response['users'] = User.objects()
        response['status'] = 1

        return response, 200
    except Exception as e:
        response['message'] = "Error while operation!"
        response['status'] = 0
        return response, 500
    

@users_blueprint.get('/users/<string:id>')
def get_user(id):
    response = {}
    try:
        user = User.objects.get(id=id).to_json()
        response['user'] = json.loads(user)
        response['status'] = 1
        return response, 200
    except DoesNotExist:
        response['message'] = "User not found!"
        response['status'] = 0
        return response, 404
    except Exception as e:
        response['message'] = "Error while operation!"
        response['status'] = 0
        return response, 500
    

@users_blueprint.post('/users')
def create_user():
    response = {}

    req_body = request.get_json()
    if req_body:
        bcrypt = Bcrypt(app)
        req_body['password'] = bcrypt.generate_password_hash(req_body.get('password')).decode('utf-8')

        User(**req_body).save()
        try:
            response['message'] = "User is created!"
            response['status'] = 1
            return response, 201
        except Exception as e:
            response['message'] = "Error while creating the user"
            response['status'] = 0
            return response, 500

    response['message'] = 'No information provided!'
    response['status'] = 0
    return response, 400


@users_blueprint.put('/users/<string:id>')
def update_user(id):
    response = {}
    try:
        data = request.get_json()
        if data.get('password'):
            response['message'] = "Password can not be updated directly!"
            response['status'] = 0
            return response, 400
        user = User.objects.get(id=id).update(**data)
        print(user)
        if user:
            response['user'] = "User updated successfully!"
            response['status'] = 1
            return response, 200
    except DoesNotExist:
        response['message'] = "User not found!"
        response['status'] = 0
        return response, 401
    except Exception as e:
        response['message'] = "Error while operation!"
        response['status'] = 0
        return response, 500

    
@users_blueprint.delete('/users/<string:id>')
def delete_user(id):
    response = {}
    try:
        user = User.objects.get(id=id).delete()
        print(user)
        response['message'] = "User deleted successfully!"
        response['status'] = 1
        return response, 200
    except DoesNotExist:
        response['message'] = "User not found!"
        response['status'] = 0
        return response, 404
    except Exception as e:
        response['message'] = "Error while operation!"
        response['status'] = 0
        return response, 500
