from flask import Flask
from flask_restful import Resource, Api, reqparse
from splitwise.recognise.receipt_reader import find_amount

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('img_string', type=str)


class ReceiptReader(Resource):
    def post(self):
        args = parser.parse_args()
        img_string = str(args['img_string'])
        res = find_amount(img_string)
        return {'amount': res}

    def get(self):
        return "Wyślij w body POST pod img_string string zawierający obraz przekonwertowany na base64 np {'img_string' : 'base64'}"


api.add_resource(ReceiptReader, '/')

if __name__ == '__main__':
    app.run(debug=True)
