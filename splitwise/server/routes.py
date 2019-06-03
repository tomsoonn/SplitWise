from flask import jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, get_jwt_identity, jwt_refresh_token_required)
from splitwise.server.app import flask_bcrypt, app, mongo
from splitwise.server.schemas import validate_bill, validate_user, validate_bill_details, validate_due
from splitwise.server import db
from splitwise.recognise.receipt_reader import find_amount


@app.route('/')
def home():
    return "home"


@app.route('/login', methods=['POST'])
def auth_user():
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        user = db.find_user(data['email'])
        if user and flask_bcrypt.check_password_hash(user['password'], data['password']):
            del user['password']
            access_token = create_access_token(identity=data)
            refresh_token = create_refresh_token(identity=data)
            user['token'] = access_token
            user['refresh'] = refresh_token
            return jsonify({'ok': True, 'data': user}), 200
        else:
            return jsonify({'ok': False, 'message': 'Invalid username or password'}), 401
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@app.route('/register', methods=['POST'])
def register():
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        user = db.find_user(data['email'])
        if user:
            return jsonify({'ok': True, 'message': 'This email is already taken'}), 401
        else:
            data['password'] = flask_bcrypt.generate_password_hash(
                data['password'])
            data['friends'] = []
            db.add_user(data)
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


# get all users in db
@app.route('/users', methods=['GET'])
@jwt_required
def get_users():
        users = db.get_users()
        return jsonify({'ok': True, 'data': users}), 200


# delete or add friend
@app.route('/friends', methods=['POST', 'GET'])
@jwt_required
def friends():
    current_user = get_jwt_identity()
    user_email = current_user['email']
    if request.method == 'GET':
        query = request.args
        user = db.find_user(query['friend'])
        if user:
            data = db.del_friend(user_email, query['friend'])
            return jsonify({'ok': True, 'data': data}), 200
        else:
            return jsonify({'ok': True, 'message': 'Cannot find user'}), 401

    data = request.get_json()
    if request.method == 'POST':
        user = db.find_user(data['friend'])
        if user:
            data = db.add_friend(user_email, data['friend'])
            return jsonify({'ok': True, 'data': data}), 200
        else:
            return jsonify({'ok': True, 'message': 'Cannot find user'}), 401


# get bill or add bill
@app.route('/bills', methods=['POST', 'GET'])
@jwt_required
def bills():
    if request.method == 'GET':
        query = request.args
        data = db.find_bill(query)
        return jsonify({'ok': True, 'data': data}), 200

    data = request.get_json()

    if request.method == 'POST':
        #user = get_jwt_identity()
        #data['owner'] = user['email']
        data = validate_bill_details(data)
        if data['ok']:
            db_response = db.add_bill(data['data'])
            return_data = mongo.db.bills.find_one({'_id': db_response.inserted_id})
            return jsonify({'ok': True, 'data': return_data}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


# analyze bill image
@app.route('/image', methods=['POST'])
@jwt_required
def analyze_image():
    data = request.get_json()
    if request.method == 'POST':
        user = get_jwt_identity()
        data['email'] = user['email']
        data = validate_bill(data)
        if data['ok']:
            bill_details = find_amount(data["bill"]) #FIXME get_bill_details
            #return_data = validate_bill_details(bill_details)
            return_data = jsonify()
            return_data['ok'] = True
            return_data['data'] = {"total_price": bill_details}
            if return_data['ok']:
                return return_data, 200
            else:
                return jsonify({'ok': False, 'message': 'Bad image analyze data: {}'.format(data['message'])}), 400
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


# find due or add due
@app.route('/dues', methods=['POST', 'GET'])
@jwt_required
def dues():
    if request.method == 'GET':
        query = request.args
        data = db.find_due(query)
        return jsonify({'ok': True, 'data': data}), 200

    data = request.get_json()
    if request.method == 'POST':
        data = validate_due(data)
        if data['ok']:
            mongo.db.bills.insert_one(data['data'])
            return jsonify({'ok': True, 'message': 'Due successfully added.'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

    return


if __name__ == '__main__':
    app.run(debug=True)
