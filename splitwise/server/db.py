from bson.objectid import ObjectId

from splitwise.server.app import mongo


def find_user(email):
    return mongo.db.users.find_one({'email': email}, {"_id": 0})


def add_user(data):
    mongo.db.users.insert_one(data)


def get_users():
    users = mongo.db.users.find({}, {"_id": 0, "password": 0})
    return to_array(users)


def del_friend(user, friend):
    return mongo.db.users.update(
        {"email": user},
        {"$pull": {"friends": friend}}
    )


def add_friend(user, friend):
    return mongo.db.users.update(
        {"email": user},
        {"$addToSet": {"friends": friend}}
    )


def set_paid(query):
    query = transform(query)
    return mongo.db.dues.update(query, {"$set": {"paid": True}})


def add_bill(data):
    return mongo.db.bills.insert_one(data)


def find_bill(query):
    query = transform(query)
    bills = mongo.db.bills.find(query)
    return to_array(bills)


def add_due(data):
    return mongo.db.dues.insert_one(data)


def find_due(query):
    query = transform(query)
    dues = mongo.db.dues.find(query)
    return to_array(dues)


def to_array(cursor):
    array = []
    for user in cursor:
        array.append(user)
    return array


def transform(query):
    if type(query) != dict:
        query = query.to_dict(flat=True)
    for e in query:
        if e == "_id":
            query[e] = ObjectId(query[e])
    return query
