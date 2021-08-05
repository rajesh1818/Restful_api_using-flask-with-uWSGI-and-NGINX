from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_restful import Api
#
app = Flask(__name__)
app1 = Api(app)
app.config['MONGO_URI']="mongodb+srv://rajesh:rajesh@imdb.8hily.mongodb.net/imdb?retryWrites=true&w=majority"
app.config["JWT_SECRET_KEY"] = "super-secret"
imdb = PyMongo(app)
jwt = JWTManager(app)

#
#
# app.config["JWT_SECRET_KEY"] = "super-secret"
# jwt = JWTManager(app)


