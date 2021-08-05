from flask import  jsonify
from flask_restful import  request
from master import imdb
from flask_jwt_extended import  get_jwt_identity





def byname(username):
    return imdb.db.user.find_one({"name": username}, {"_id": 0, "name": 1, "email": 1})


def get_user(email):
    try:
        return imdb.db.user.find_one({"email": email}, {"_id": 0})
    except Exception as e:
        return {"error": e}



def add(data):
    currentUser = get_jwt_identity()

    name = data["name"]
    email = data["email"]
    password =data["password"]
    if not currentUser['isadmin']:
        return jsonify({'message': 'Cannot perform that function!'})

    return imdb.user.insert_one({"name":name,"email":email,"password":password,"isadmin":False,"role":"role not assigned"})


def delete():
    currentUser = get_jwt_identity()

    if not currentUser['isadmin']:
        return jsonify({'message': 'Cannot perform that function!'})
    data = request.get_json()
    imdb.db.user.delete_one(data)
    return jsonify({'message': 'User deleted successfully'})


def update(username):
    currentUser = get_jwt_identity()

    if not currentUser['isadmin']:
        return jsonify({'message': 'Cannot perform that function!'})

    data = request.get_json()
    updateduser = data['name']
    return  imdb.db.user.update_one({"name": username}, {"$set": {"name": updateduser}})

