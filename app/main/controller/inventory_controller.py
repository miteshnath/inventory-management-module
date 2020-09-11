from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..service.inventory_service import get_all_inventories, save_new_inventory, get_an_inventory, update_inventory, delete_inventory_method
from ..util.dto import InventoryDto

api = InventoryDto.api
inventory = InventoryDto.inventory
post_inventory = InventoryDto.post_inventory
put_inventory = InventoryDto.put_inventory


@api.route('/')
class InventoryList(Resource):
    @api.doc('list_of_inventories')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @admin_token_required
    @api.marshal_list_with(inventory, envelope='data')
    def get(self):
        return get_all_inventories()
    
    @api.expect(post_inventory, validate=True)
    @api.response(201, 'Inventory successfully created.')
    @api.doc('create a new inventory')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @admin_token_required
    def post(self):
        """Creates a new Inventory """
        data = request.json
        return save_new_inventory(data=data)
    

@api.route('/<id>')
@api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
@api.param('id', 'Inventory identifier')
@api.response(404, 'Inventory not found.')
class Inventory(Resource):
    @api.doc('get an inventory')
    @api.marshal_with(inventory)
    def get(self, id):
        """get an inventory given its identifier"""
        _inventory = get_an_inventory(id)
        if not _inventory:
            api.abort(404)
        else:
            return _inventory, 200
        
    
    @api.doc('update an inventory')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @api.expect(put_inventory, validate=True)
    @api.response(200, 'Inventory successfully updated.')
    @admin_token_required
    def put(self, id):
        """Update an Inventory """
        _inventory = get_an_inventory(id)
        if not _inventory:
            api.abort(404)
        else:
            data = request.json
            data['id'] = id
            data['store_id'] = _inventory.store_id
            return update_inventory(data=data)
        
    @api.doc('delete an inventory')
    @api.response(204, 'Inventory successfully deleted.')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @admin_token_required
    def delete(self, id):
        """Delete an inventory given its identifier"""
        _invent = get_an_inventory(id)
        if not _invent:
            api.abort(404)
        else:
            return delete_inventory_method(_invent.id)
