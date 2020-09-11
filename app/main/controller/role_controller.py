from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..service.role_service import get_all_roles, save_new_role, get_a_role
from ..util.dto import RoleDto

api = RoleDto.api
role = RoleDto.role


@api.route('/')
class RoleList(Resource):
    @api.doc('list_of_roles')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @admin_token_required
    @api.marshal_list_with(role, envelope='data')
    def get(self):
        return get_all_roles()
    
    @api.expect(role, validate=True)
    @api.response(201, 'Role successfully created.')
    @api.doc('create a new role')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @admin_token_required
    def post(self):
        """Creates a new Role """
        data = request.json
        return save_new_role(data=data)
    


@api.route('/<id>')
@api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
@api.param('id', 'Role identifier')
@api.response(404, 'Role not found.')
class Role(Resource):
    @api.doc('get a role')
    @api.marshal_with(role)
    def get(self, id):
        """get a brand given its identifier"""
        _role = get_a_role(id)
        if not _role:
            api.abort(404)
        else:
            return _role, 200