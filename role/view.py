from flask_restful import Resource, Api, request
from flask import  Blueprint, jsonify,make_response
from .controller import add_role,deleterole,finduserrole,update_role
from flask_jwt_extended import jwt_required


api_role = Blueprint('role', __name__)
api = Api(api_role)




class addrole(Resource):
    @jwt_required
    def post(self):
        data=request.get_json()

        try:

            add_role(data)
            return jsonify({'message': 'role added successfully'})

        except Exception as e:
            response_object = {
                'error': {'internal': e}
            }
            return make_response(jsonify(response_object)), 500


class updateuserrole(Resource):
    @jwt_required
    def post(self):
        data=request.get_json()

        try:

            a=update_role(data)
            if a==0:
                return jsonify({'message': 'this user has no role assigned you should first add role first!'})
            return jsonify({'message': 'role updated successfully'})

        except Exception as e:
            response_object = {
                'error': {'internal': e}
            }
            return make_response(jsonify(response_object)), 500

class deleteuserrole(Resource):
    @jwt_required

    def post(self):
        try:
            deleterole()
            return ('role deleted successfully!!')
        except Exception as e:
            response_object = {
                'error': {'internal': str(e)}
            }
            return make_response(jsonify(response_object)), 401



class getusersrole(Resource):
    @jwt_required


    def post(self):
        data = request.get_json()
        email = data['email']
        data = request.get_json()
        try:
            b=finduserrole(data)
            return (b)
        except Exception as e:
            response_object = {
                'error': {'internal': str(e)}
            }
            return make_response(jsonify(response_object)), 401






api.add_resource(addrole, '/addrole')
api.add_resource(deleteuserrole, '/deleterole')
api.add_resource(getusersrole, '/getrole')
api.add_resource(updateuserrole, '/updaterole')
