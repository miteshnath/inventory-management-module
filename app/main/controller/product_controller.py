from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..service.product_service import get_all_products, save_new_product, get_a_product, update_product, delete_product_method
from ..util.dto import ProductDto

api = ProductDto.api
product = ProductDto.product
post_product = ProductDto.post_product
put_product = ProductDto.put_product


@api.route('/')
class ProductList(Resource):
    @api.doc('list_of_products')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @admin_token_required
    @api.marshal_list_with(product, envelope='data')
    def get(self):
        return get_all_products()
       
    @api.expect(post_product, validate=True)
    @api.response(201, 'Product successfully created.')
    @api.doc('create a new product')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @admin_token_required
    def post(self):
        """Creates a new Product """
        data = request.json
        return save_new_product(data=data)
    


@api.route('/<id>')
@api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
@api.param('id', 'Product identifier')
@api.response(404, 'Product not found.')
class Product(Resource):
    @api.doc('get a product')
    @api.marshal_with(product)
    def get(self, id):
        """get a product given its identifier"""
        _product = get_a_product(id)
        if not _product:
            api.abort(404)
        else:
            return _product, 200
        
    @api.doc('update a product')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @api.expect(put_product, validate=True)
    @api.response(200, 'Product successfully updated.')
    @api.response(404, 'Product not found.')
    @admin_token_required
    def put(self, id):
        """Update a Product """
        _prod = get_a_product(id)
        if not _prod:
            api.abort(404)
        else:
            data = request.json
            data['id'] = id
            data['brand_id'] = _prod.brand_id
            return update_product(data=data)
        
    @api.doc('delete a product')
    @api.response(204, 'Product successfully deleted.')
    @api.response(404, 'Product not found.')
    @api.response(400, 'Product can\'t be deleted because of existing foreign key mappings.')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @admin_token_required
    def delete(self, id):
        """Delete a product given its identifier"""
        _prod = get_a_product(id)
        if not _prod:
            api.abort(404)
        else:
            return delete_product_method(_prod.id)