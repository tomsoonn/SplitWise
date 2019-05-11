from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

user_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
            "minLength": 5
        }
    },
    "required": ["email", "password"],
    "additionalProperties": False
}


def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}


bill_schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string"
        },
        "price": {
            "type": "float"
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "owner": {
            "type": "string",
        },
        "participants": {
            "type": "array",
            "additionalItems": {"type": "string"},
            "uniqueItems": True

        }
    },
    "required": ["email", "status", "title"],
    "additionalProperties": False
}


def validate_bill(data):
    try:
        validate(data, bill_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}