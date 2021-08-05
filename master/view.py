from flask import  jsonify,make_response,Blueprint
from flask_restful import Resource, Api, request
from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token
# from myproject.master import app
from master.controller import login_user,logout_user,add,get_user,password
# from myproject.user.view import api_route
# from myproject.role.view import api_role


api_view = Blueprint('view', __name__)
app1 = Api(api_view)

class login(Resource):

    def post(self):
        email = ""
        password = ""
        try:
            post_data = request.get_json()
            email = post_data['email']
            password = post_data['password']

        except Exception as e:
            jsonify({'error': str(e)}), 400

        userdata = get_user(email)
        if not userdata:
            return jsonify(error="incorrect email id")
        reqPassword = userdata["password"]
        isAdmin = userdata["isadmin"]

        if not (reqPassword == password):
            return jsonify(error="incorrect password")


        tokenBody = {"email": email, "isadmin": isAdmin,"password":password}

        access_token = create_access_token(identity=tokenBody)

        try:
            login_user(email, access_token)

            return jsonify(token=access_token)
        except Exception as e:
            response_object = {
                'error': {'internal': e}
            }
            return make_response(jsonify(response_object)), 500

class logout(Resource):
    @jwt_required
    def post(self):
        currentUser = get_jwt_identity()
        try:
            logout_user(currentUser["email"])

            return jsonify(status="Logout"), 201
        except Exception as e:
            response_object = {
                'error': {'internal': str(e)}
            }
            return make_response(jsonify(response_object)), 401

class register(Resource):
    def post(self):
        try:
            data = request.get_json()
            user_email = data["email"]
            userdata = get_user(user_email)
            if userdata:
                return jsonify(error="This User is Already Registered")

            add(data)
            return jsonify({'message': 'User registered successfully'})

        except Exception as e:
            response_object = {
                'error': {'internal': str(e)}
            }
            return make_response(jsonify(response_object)), 401

class updatepassword(Resource):
    @jwt_required
    def post(self):
        data=request.get_json()
        password(data)
        return ('password updated successfullyy!!!!')




app1.add_resource(login, '/login')
app1.add_resource(logout, '/logout')
app1.add_resource(register, '/register')
app1.add_resource(updatepassword, '/updatepassword')

# app.register_blueprint(api_route)
# app.register_blueprint(api_view)
# app.register_blueprint(api_role)

#
# if __name__ == '__main__':
#     app.run(debug=True)