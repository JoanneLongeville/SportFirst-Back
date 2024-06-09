
from connectors import database
from connectors.authentication import handle_register_post
from http.server import HTTPServer, BaseHTTPRequestHandler
from middleware import handle_cors_headers
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class AccountResource(Resource):
    def post(self):
        data = request.get_json()
        response_data, response_code = handle_register_post(data)
        return response_data, response_code

api.add_resource(AccountResource, '/accounts')

if __name__ == "__main__":
    database.create_table()
    app.run(debug=True)
