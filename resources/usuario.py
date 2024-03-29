from sqlite3 import IntegrityError
from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
from flask import make_response, render_template
import traceback


atributos = reqparse.RequestParser()
atributos.add_argument('login', 
                        type=str, 
                        required=True,
                        help='The field login cannot be blank'
                        )
atributos.add_argument('senha', 
                        type=str, 
                        required=True,
                        help='The field senha cannot be blank'
                        )
atributos.add_argument('email', type=str)
atributos.add_argument('ativo', default=False, type=bool)


class User(Resource):   
    # /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @jwt_required
    def delete(self, user_id):
        
        user = UserModel.find_user(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        try:
            user.delete_user()
        except:
            return {'message': 'An internal error ocurred trying to delete User.'}, 500 # Internal server error.     
        
        return {'message': 'User deleted'}, 200


class UserRegister(Resource):
    # /cadastro
    def post(self):
        dados = atributos.parse_args()
        if not dados.get('email') or dados.get('email') is None:
            return {'message': 'Must have email field.'}, 400

        if UserModel.find_by_login(dados['login']):
            return {'message': f"The login '{dados['login']}' already exists"}, 400

        if UserModel.find_by_email(dados['email']):
            return {'message': f"The email '{dados['email']}' already exists"}, 400

        user = UserModel(**dados)
        user.ativo = False
        try:
            user.save_user()
            resp = user.send_confirmation_email()
            print('VaiCARAI', resp.status_code)
        except:
            user.delete_user()
            traceback.print_exec()
            return {'message': 'An internal server error has oourred'}   
        return {'message': 'User created successfully!'}, 201 #Created


class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])
        if not user or not safe_str_cmp(user.senha, dados['senha']):
            return {'message': 'User or Password incorrect!'}, 401 #Unauthorized
        if not user.ativo:
            return {'message': 'User not activated!'}, 401 #Unauthorized
        token_de_acesso = create_access_token(identity=user.user_id)
        return {'access_token': token_de_acesso}, 200


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti'] #JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully' }


class UserConfirm(Resource):
    #/confirmacao/{user_id}
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user(user_id)
        if not user:
            {'message': f'User id {user_id} not found'}, 404
        user.ativo = True
        user.save_user()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('user_confirm.html', email=user.email, login=user.login), 200, headers)
        #return {'message': f'User id {user_id} confimed successfully'}, 200