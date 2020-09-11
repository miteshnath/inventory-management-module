from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..service.item_service import get_all_items, save_new_item, get_an_item, update_item, delete_item_method
from ..util.dto import ItemDto

api = ItemDto.api
item = ItemDto.item
post_item = ItemDto.post_item
put_item = ItemDto.put_item


@api.route('/')
class ItemList(Resource):
    @api.doc('list_of_items')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @admin_token_required
    @api.marshal_list_with(item, envelope='data')
    def get(self):
        return get_all_items()
    
    @api.doc('create a new item')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})       
    @api.expect(post_item, validate=True)
    @api.response(201, 'Item successfully created.')
    @admin_token_required
    def post(self):
        """Creates a new Item """
        data = request.json
        return save_new_item(data=data)
    


@api.route('/<id>')
@api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
@api.param('id', 'Item identifier')
@api.response(404, 'Item not found.')
class Item(Resource):
    @api.doc('get an item')
    @admin_token_required
    @api.marshal_with(item)
    def get(self, id):
        """get an item given its identifier"""
        _item = get_an_item(id)
        if not _item:
            api.abort(404)
        else:
            return _item, 200
        
    @api.doc('update an item')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @api.expect(put_item, validate=True)
    @api.response(200, 'Item successfully updated.')
    @api.response(404, 'Item not found.')
    @admin_token_required
    def put(self, id):
        """Update an Item """
        _item = get_an_item(id)
        if not _item:
            api.abort(404)
        else:
            data = request.json
            data['id'] = id
            data['product_id'] = _item.product_id
            return update_item(data=data)
        
    @api.doc('delete an item')
    @api.response(204, 'Item successfully deleted.')
    @api.response(404, 'Item not found.')
    @api.response(400, 'Item can\'t be deleted because of existing foreign key mappings.')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @admin_token_required
    def delete(self, id):
        """Delete an item given its identifier"""
        _item = get_an_item(id)
        if not _item:
            api.abort(404)
        else:
            return delete_item_method(_item.id)
        
    