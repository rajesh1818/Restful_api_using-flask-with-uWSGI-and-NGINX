
from flask import jsonify
from flask_jwt_extended import  get_jwt_identity
from . import imdb




def get_user(email):
    try:
        return imdb.db.user.find_one({"email": email}, {"_id": 0})

    except Exception as e:
        return {"error": e}


def login_user(email, access_token):
    try:
        imdb.db.session.update_one({"email": email}, {"$set": {"jwt": access_token}}, upsert=True)
        return {"success": True}
    except Exception as e:
        return {"error": e}

def add(data):
    currentUser = get_jwt_identity()

    name = data["name"]
    email = data["email"]
    password =data["password"]
    if not currentUser['isadmin']:
        return jsonify({'message': 'Cannot perform that function!'})

    return imdb.db.user.insert_one({"name":name,"email":email,"password":password,"isadmin":False,"role":"role not assigned"})


def logout_user(email):
    try:
        imdb.db.session.delete_one({"email": email})
        return {"success": True}
    except Exception as e:
        return {"error": e}

def password(data):
    email=data['email']
    newpassword = data['newpassword']
    return  imdb.db.user.update_one({"email": email}, {"$set": {"password": newpassword}})