
from flask import Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required
from flask_restful import Resource, Api, request

from .controller import get_user, add, delete, update, byname

api_route = Blueprint('route', __name__)
apir = Api(api_route)



class adduser(Resource):
    @jwt_required
    def post(self):
        try:
            data = request.get_json()

            user_email = data["email"]
            userdata = get_user(user_email)
            if userdata:
                return jsonify(error="username is already taken")
            add(data)
            return jsonify({'message': 'User Added successfully'})
        except Exception as e:
            response_object = {
                'error': {'internal': str(e)}
            }
            return make_response(jsonify(response_object)), 401


class userbyname(Resource):

    def get(self, username):
        try:
            a = byname(username)
            return jsonify(a)
        except Exception as e:
            response_object = {
                'error': {'internal': str(e)}
            }
            return make_response(jsonify(response_object)), 401

class deleteuser(Resource):
    @jwt_required

    def post(self):
        try:
            d = delete()
            return ('user deleted successfully!!')
        except Exception as e:
            response_object = {
                'error': {'internal': str(e)}
            }
            return make_response(jsonify(response_object)), 401

class updateuser(Resource):
    @jwt_required

    def post(self, username):
        try:
            a = update(username)
            return ('users name updated successfullyy!!!!')
        except Exception as e:
            response_object = {
                'error': {'internal': str(e)}
            }
            return make_response(jsonify(response_object)), 401





apir.add_resource(userbyname, '/user/<username>')
apir.add_resource(adduser, '/adduser')
apir.add_resource(deleteuser, '/deleteuser')
apir.add_resource(updateuser, '/updateuser/<username>')