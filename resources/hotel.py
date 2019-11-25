import sqlite3
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from flask_jwt_extended import jwt_required
from resources.filtros import normalize_path_params, consulta


class Hoteis(Resource):
    # path hoteis?cidade=Rio de Janeiro&estrelas_min=4&diaria_max=400
    consulta = consulta
    path_params = reqparse.RequestParser()
    path_params.add_argument('estrelas_min', type=float)
    path_params.add_argument('estrelas_max', type=float)
    path_params.add_argument('diaria_min', type=float)
    path_params.add_argument('diaria_max', type=float)
    path_params.add_argument('cidade', type=str)
    path_params.add_argument('limit', type=float)
    path_params.add_argument('offset', type=float)  

    def get(self):

        #hoteis = HotelModel.query.all()
        #return {"hoteis": [hotel.json() for hotel in hoteis ]}       
        
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()
        
        dados = self.path_params.parse_args()
        
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)
        
        if not parametros.get('cidade'):
            self.consulta += 'LIMIT ? OFFSET ?'
        else:
            self.consulta += 'AND cidade = ? LIMIT ? OFFSET ?'
        
        tupla = tuple([parametros[chave] for chave in parametros])
        print(tupla)
        resultado = cursor.execute(self.consulta, tupla)            
        
        hoteis = []
        for linha in resultado:
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4],
                'site_id': linha[5]})

        return {'hoteis': hoteis}


class Hotel(Resource):   
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome',
                            type=str, 
                            required=True, 
                            help="The Field 'nome' cannot be blank"
                            )

    argumentos.add_argument('estrelas', 
                            type=float, 
                            required=True, 
                            help="The Field 'esrelas' cannot be blank",
                            )
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    argumentos.add_argument('site_id', type=int, required=True, help='Every hotel needs to be linked a site')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if not hotel:
            return {'message': 'Hotel not found'}, 404
        return hotel.json()

    @jwt_required
    def post(self, hotel_id):

        dados = self.argumentos.parse_args()
        
        if HotelModel.find_hotel(hotel_id) and HotelModel.find_hotel_by_site_id(dados.get('site_id')):
            return {'message': f"Hotel id '{hotel_id}' already exists."}, 400 #bad request


        if not SiteModel.find_by_id(dados.get('site_id')):
            return {'message': 'The hotel must be associated to valid site id'}, 400

        
        try:
            nome = dados.get('nome').strip()
        except:
            nome = None    

        if not nome:
            return {'message': 'The field name cannot be blank or null'}
        
        hotel = HotelModel(hotel_id, **dados)
        
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 # Internal server error.
        return hotel.json()

    @jwt_required
    def put(self, hotel_id):
        dados = self.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        
        if not hotel_encontrado:
            
            hotel = HotelModel(hotel_id, **dados)
            try:
                hotel.save_hotel()
            except:
                return {'message': 'An internal error ocurred trying to save hotel.'}, 500 # Internal server error.
            return hotel.json(), 201  # created

        hotel_encontrado.update_hotel(**dados)
        try:
            hotel_encontrado.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 # Internal server error.
        return hotel_encontrado.json(), 200 #ok
    
    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if not hotel:
            return {'message': 'Hotel not found'}, 404
        try:
            hotel.delete_hotel()
        except:
            return {'message': 'An internal error ocurred trying to delete hotel.'}, 500 # Internal server error.     
        return {'message': 'Hotel deleted'}, 200