import datetime
import logging

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo

from splitwise.server.json_encoder import JSONEncoder

logger = logging.getLogger(__name__)
app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/SplitwiseDatabase"
app.config['JWT_SECRET_KEY'] = 'SECRET'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.json_encoder = JSONEncoder

mongo = PyMongo(app)
flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)

logger.debug('App loaded')