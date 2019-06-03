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

bill_schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string"
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "bill": {
            "type": "string"
        },
        "participants": {
            "type": "array",
            "additionalItems": {"type": "string"},
            "uniqueItems": True
        }
    },
    "required": ["email", "price", "title"],
    "additionalProperties": False
}

bill_details_schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string"
        },
        "owner": {
            "type": "string",
            "format": "email"
        },
        "total_price": {
            "type": "number"
        },
        "date": {
            "type": "string",
            "format": "date"
        },
        "products": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                  "name": {
                    "type": "string"
                  },
                  "price": {
                    "type": ["number"]
                  }
                },
                "required": [
                  "name", "price"
                ]
            }
        },
    },
    "required": ["total_price"], #FIXME required all
    "additionalProperties": False
}

due_schema = {
    "type": "object",
    "properties": {
        "due_from": {
            "type": "string",
            "format": "email"
        },
        "due_to": {
            "type": "string",
            "format": "email"
        },
        "amount": {
            "type": "number"
        },
        "bill_id": {
            "type": "string",
        },
        "product": {
            "type": "string",
        },
        "paid": {
            "type": "boolean"
        }
    },
    "required": ["due_from", "due_to", "amount", "bill_id", "product", "paid"],
    "additionalProperties": False
}


def validate_user(data):
    return validate_schema(data, user_schema)


def validate_bill(data):
    return validate_schema(data, bill_schema)


def validate_bill_details(data):
    return validate_schema(data, bill_details_schema)


def validate_due(data):
    return validate_schema(data, due_schema)


def validate_schema(data, schema):
    try:
        validate(data, schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
