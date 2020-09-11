from flask import request
from flask_restx import Resource

from app.main.service.auth_helper import Auth
from ..service.user_service import save_new_user
from ..util.dto import AuthDto

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/register')
class UserRegister(Resource):
    """
        User Register Resource
    """
    @api.doc('user register')
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        data = request.json
        return save_new_user(data=data)
    
    
@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)
