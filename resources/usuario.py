from sqlite3 import IntegrityError
from flask_restful import Resource, reqparse
from models.usuario import UserModel


class User(Resource):   
    
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if not user:
            return {'message': 'Hotel not found'}, 404
        return user.json()

    
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if not user:
            return {'message': 'Hotel not found'}, 404
        try:
            user.delete_user()
        except:
            return {"message": "An internal error ocurred trying to delete hotel."}, 500 # Internal server error.     
        return {'message': 'Hotel deleted'}, 200