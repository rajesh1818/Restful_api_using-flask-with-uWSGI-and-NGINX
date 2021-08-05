import datetime
import uuid
from flask import  jsonify
from flask_restful import  request
from master import imdb
from flask_jwt_extended import  get_jwt_identity

time = datetime.datetime.now()


def finduserrole(data):
        try:
            role_id =imdb.db.user.find_one({'email': data['email']}, {"_id": 0, 'role_id': 1})
            a=role_id.get('role_id')
            if a=='FALSE':
                return jsonify({'message': 'This user has no role'})
            role_id = imdb.db.user.find_one({'email':data['email']},{"_id":0,'role_id':1})
            return imdb.db.role.find_one({'role_id': role_id.get('role_id')},{"_id":0,'role_name':1,'given_by':1})
        except Exception as e:
                return {"error": e}


def add_role(data):
        currentUser = get_jwt_identity()
        role_id = uuid.uuid1()
        useremail = currentUser['email']
        u=imdb.db.user.find_one({'email':useremail}, {'_id':0,'name':1})
        given_by=u.get('name')

        role_name = data["role_name"]
        email= data['email']

        if not currentUser['isadmin']:
            return jsonify({'message': 'Cannot perform that function!'})

        imdb.db.role.insert_one({'role_id':role_id,'given_by':given_by,'role_name':role_name,'time':time})
        return imdb.db.user.update_one({'email': email},{'$set': {'role_id': role_id}},upsert=True)


def update_role(data):
    currentUser = get_jwt_identity()
    role_id = imdb.db.user.find_one({'email': data['email']}, {"_id": 0, 'role_id': 1})
    useremail = currentUser['email']
    u = imdb.db.user.find_one({'email': useremail}, {'_id': 0, 'name': 1})
    given_by = u.get('name')
    role_name = data["role_name"]

    if not currentUser['isadmin']:
        return jsonify({'message': 'Cannot perform that function!'})

    if not role_id.get('role_id'):
        return 0
    return  imdb.db.role.update_one({'role_id': role_id.get('role_id')}, {  '$set': {'given_by': given_by, 'role_name': role_name,'time': time}}, upsert=True)




def deleterole():
    currentUser = get_jwt_identity()

    if not currentUser['isadmin']:
        return jsonify({'message': 'Cannot perform that function!'})
    data = request.get_json()
    role_id =imdb.db.user.find_one({'email':data['email']},{"_id":0,'role_id':1})
    imdb.db.role.delete_one({'role_id':role_id.get('role_id')})
    imdb.db.user.update_one({'email': data['email']}, {'$set': {'role_id': 'FALSE'}}, upsert=True)
    return jsonify({'message': 'User deleted successfully'})





