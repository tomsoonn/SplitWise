from bson import ObjectId
from flask import jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, get_jwt_identity, jwt_refresh_token_required)
from splitwise.server.app import flask_bcrypt, app, mongo
from splitwise.server.schemas import validate_bill, validate_user
import logging

logger = logging.getLogger(__name__)


@app.route('/')
def home():
    return "hello world"


@app.route('/login', methods=['POST'])
def auth_user():
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        user = mongo.db.users.find_one({'email': data['email']}, {"_id": 0})
        if user and flask_bcrypt.check_password_hash(user['password'], data['password']):
            del user['password']
            access_token = create_access_token(identity=data)
            refresh_token = create_refresh_token(identity=data)
            user['token'] = access_token
            user['refresh'] = refresh_token
            return jsonify({'ok': True, 'data': user}), 200
        else:
            return jsonify({'ok': False, 'message': 'invalid username or password'}), 401
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@app.route('/register', methods=['POST'])
def register():
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        data['password'] = flask_bcrypt.generate_password_hash(
            data['password'])
        mongo.db.users.insert_one(data)
        return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'token': create_access_token(identity=current_user)
    }
    return jsonify({'ok': True, 'data': ret}), 200


@app.route('/bills', methods=['POST', 'GET'])
@jwt_required
def bills():
    if request.method == 'GET':
        query = request.args
        try:
            data = mongo.db.bills.find_one({'_id': ObjectId(query['id'])})
        except KeyError:
            data = list(mongo.db.bills.find({'email': query['email']}))
        return jsonify({'ok': True, 'data': data}), 200

    data = request.get_json()

    if request.method == 'POST':
        user = get_jwt_identity()
        data['email'] = user['email']
        data = validate_bill(data)
        if data['ok']:
            db_response = mongo.db.bills.insert_one(data['data'])
            return_data = mongo.db.bills.find_one({'_id': db_response.inserted_id})
            return jsonify({'ok': True, 'data': return_data}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        data = request.get_json()
        type_ = data['type']
        email = data['email']
        friendName = data['friendName']
        if type_ == 'ADD':
            logger.debug("ADD users")  # TODO add friend
        elif type_ == 'REM':
            logger.debug("REM users")  # TODO remove friend
        return jsonify({'ok': True})

    if request.method == 'GET':
        data = request.get_json()
        try:
            forUser = data['email']
        except KeyError:  # TODO extract all users
            return jsonify({'ok': True, 'data': [{'name': 'ala'}, {'name': 'kot'}]})
        else:  # TODO extract friends of users with email
            return jsonify({'ok': True, 'data': [{'name': 'pies'}]})


if __name__ == '__main__':
    app.run(debug=True)
