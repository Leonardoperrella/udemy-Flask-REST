from sqlalchemy.exc import IntegrityError

from sql_alchemy import banco


class UserModel(banco.Model):
    __tablename__ = 'usuarios'
    
    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))
    ativo = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, senha, ativo):

       self.login = login
       self.senha = senha 
       self.ativo = ativo
       
    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
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

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()

         




