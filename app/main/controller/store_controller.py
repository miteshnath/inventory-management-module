from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..service.store_service import get_all_stores, save_new_store, get_a_store
from ..util.dto import StoreDto

api = StoreDto.api
store = StoreDto.store


@api.route('/')
class StoreList(Resource):
    @api.doc('list_of_stores')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @api.marshal_list_with(store, envelope='data')
    def get(self):
        return get_all_stores()
    
    @api.expect(store, validate=True)
    @admin_token_required
    @api.response(201, 'Store successfully created.')
    @api.doc('create a new store')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    def post(self):
        """Creates a new Store """
        data = request.json
        return save_new_store(data=data)
    


@api.route('/<id>')
@api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
@api.param('id', 'Store identifier')
@api.response(404, 'Store not found.')
class Store(Resource):
    @api.doc('get a store')
    @api.marshal_with(store)
    def get(self, id):
        """get a store given its identifier"""
        _store = get_a_store(id)
        if not _store:
            api.abort(404)
        else:
            return _store, 200