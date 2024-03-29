from sqlalchemy.exc import IntegrityError
from models.site import SiteModel 
from sql_alchemy import banco


class HotelModel(banco.Model):
    __tablename__ = 'hoteis'
    
    hotel_pk = banco.Column(banco.Integer, primary_key=True)
    hotel_id = banco.Column(banco.String)
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))
    site_id = banco.Column(banco.Integer, banco.ForeignKey('sites.site_id'))

    def __init__(self, hotel_id, nome, estrelas, diaria, cidade, site_id):

        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.site_id = site_id

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade,
            'site_id': self.site_id
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first() #SELECT * FROM hoteis where hotel_id = hotel_id limmit 1
        if hotel:
            return hotel

    @classmethod
    def find_hotel_by_site_id(cls, site_id):
        hotel = cls.query.filter_by(site_id=site_id).first() #SELECT * FROM hoteis where hotel_id = hotel_id limmit 1
        if hotel:
            return hotel        

    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, nome, estrelas, diaria, cidade):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()

         



