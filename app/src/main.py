from connectors import database
from connectors.authentication import handle_register_post, handle_login_post
from connectors.authentication import handle_profile_get
from connectors.calendar import handle_reservation_post
from connectors.calendar import handle_reservation_delete
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)


class AccountResource(Resource):
    def post(self):
        data = request.get_json()
        response_data, response_code = handle_register_post(data)
        return response_data, response_code


class LoginRessource(Resource):
    def post(self):
        data = request.get_json()
        response_data, response_code = handle_login_post(data)
        return response_data, response_code


class ReservationRessource(Resource):
    def post(self):
        data = request.get_json()
        response_data, response_code = handle_reservation_post(data)
        return response_data, response_code


class ReadResource(Resource):
    def get(self):
        data = request.get_json()
        response_data, response_code = handle_profile_get(data)
        return response_data, response_code


class DeleteReservation(Resource):
    def delete(self):
        data = request.get_json()
        response_data, response_code = handle_reservation_delete(data)
        return response_data, response_code


api.add_resource(AccountResource, '/accounts')
api.add_resource(LoginRessource, '/login')
api.add_resource(ReadResource, '/profile')
api.add_resource(ReservationRessource, '/reservations')
api.add_resource(DeleteReservation, '/reservations')

if __name__ == "__main__":
    database.create_table()
    app.run(debug=True)
