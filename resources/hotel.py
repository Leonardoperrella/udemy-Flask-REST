from sqlite3 import IntegrityError
from flask_restful import Resource, reqparse
from models.hotel import HotelModel


class Hoteis(Resource):
    def get(self):
        hoteis = HotelModel.query.all()
        return {'hoteis': [hotel.json() for hotel in hoteis ]}


class Hotel(Resource):   
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome',
                            type=str, 
                            required=True, 
                            help="The Field 'nome' cannot be blank",
                            )

    argumentos.add_argument('estrelas', 
                            type=float, 
                            required=True, 
                            help="The Field 'esrelas' cannot be blank",
                            )
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

        try:
            nome = dados.get('nome').strip()
        except:
            nome = None    

        if not nome:
            return {"message": "The field name cannot be blank or null"}

        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {"message": "An internal error ocurred trying to save hotel."}, 500 # Internal server error.
        return hotel.json()

    def put(self, hotel_id):
        dados = self.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        
        if not hotel_encontrado:
            
            hotel = HotelModel(hotel_id, **dados)
            try:
                hotel.save_hotel()
            except:
                return {"message": "An internal error ocurred trying to save hotel."}, 500 # Internal server error.
            return hotel.json(), 201  # created

        hotel_encontrado.update_hotel(**dados)
        try:
            hotel_encontrado.save_hotel()
        except:
            return {"message": "An internal error ocurred trying to save hotel."}, 500 # Internal server error.
        return hotel_encontrado.json(), 200 #ok

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if not hotel:
            return {'message': 'Hotel not found'}, 404
        try:
            hotel.delete_hotel()
        except:
            return {"message": "An internal error ocurred trying to delete hotel."}, 500 # Internal server error.     
        return {'message': 'Hotel deleted'}, 200