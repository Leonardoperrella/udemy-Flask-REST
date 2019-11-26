from sqlalchemy.exc import IntegrityError
from sql_alchemy import banco
from flask import request, url_for
import requests

MAILGUN_DOMAIN = 'sandboxbccbec7b0c9946a191ed1ff59efea218.mailgun.org'
MAILGUN_API_KEY = 'd5b9d2b090c3374e8ddf97b9d226b856-e470a504-f0af0c70'
FROM_TITLE = 'No reply'
FROM_EMAIL = 'no-reply@restapihoteis.com'


class UserModel(banco.Model):
    __tablename__ = 'usuarios'
    
    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    ativo = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, senha, email, ativo):

       self.login = login
       self.senha = senha 
       self.email = email
       self.ativo = ativo

    def send_confirmation_email(self):
        # /confirmacao/{user_id}

        link = request.url_root[:-1] + url_for('userconfirm', user_id=self.user_id)
        return requests.post(f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages',
                    auth=('api', MAILGUN_API_KEY),
                    data={'from': f'{FROM_TITLE} <{FROM_EMAIL}>',
                        'to': self.email,
                        'subject':'Confirmacao de cadastro',
                        'text': f'Confirme seu cadastro clicando no link a seguir {link}',
                        'html': f'<html><p>\
                        Confirme seu cadastro clicando no link a seguir: <a href="{link}">CONFIRMAR EMAIL</a>\
                        </p></html>'}
                    )   
    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'email': self.email,
            'ativo': self.ativo
        }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first() #SELECT * FROM hoteis where hotel_id = hotel_id limmit 1
        if user:
            return user

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user

    @classmethod
    def find_by_email(cls, email):
        email = cls.query.filter_by(email=email).first()
        if email:
            return email        

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()

         




