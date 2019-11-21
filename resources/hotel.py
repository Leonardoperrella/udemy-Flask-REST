from sqlite3 import IntegrityError
from flask_restful import Resource, reqparse
from models.hotel import HotelModel


class Hoteis(Resource):
    def get(self):
        hoteis = HotelModel.query.all()
        return {'hoteis': [hotel.json() for hotel in hoteis ]}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if not hotel:
            return {'message': 'Hotel not found'}, 404
        return hotel.json()

    def post(self, hotel_id):

        if HotelModel.find_hotel(hotel_id):
            return {"message": f"Hotel id '{hotel_id}' already exixts."}, 400 #bad request

        dados = self.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json()

    def put(self, hotel_id):
        dados = self.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        
        if not hotel_encontrado:
            
            hotel = HotelModel(hotel_id, **dados)
            hotel.save_hotel()
            return hotel.json(), 201  # created

        hotel_encontrado.update_hotel(**dados)
        hotel_encontrado.save_hotel()
        return hotel_encontrado.json(), 200 #ok

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if not hotel:
            return {'message': 'Hotel not found'}, 404
        hotel.delete_hotel()
        return {'message': 'Hotel deleted'}, 200