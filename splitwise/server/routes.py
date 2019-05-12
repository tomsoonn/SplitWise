from bson import ObjectId
from flask import jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, get_jwt_identity, jwt_refresh_token_required)
from splitwise.server.app import flask_bcrypt, app, mongo
from splitwise.server.schemas import validate_bill, validate_user


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
        data = mongo.db.bills.find_one({'_id': ObjectId(query['id'])})
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


if __name__ == '__main__':
    app.run(debug=True)
