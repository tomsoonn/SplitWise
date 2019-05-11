import datetime
import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo

from splitwise.server.json_encoder import JSONEncoder

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/myDatabase"
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.json_encoder = JSONEncoder

mongo = PyMongo(app)
flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)
