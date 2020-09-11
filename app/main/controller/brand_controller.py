from flask import request
from flask_restx import Resource


from app.main.util.decorator import admin_token_required
from ..service.brand_service import get_all_brands, save_new_brand, get_a_brand, update_brand, delete_brand_method
from ..util.dto import BrandDto

api = BrandDto.api
brand = BrandDto.brand
post_brand = BrandDto.post_brand
put_brand = BrandDto.put_brand


@api.route('/')
class BrandList(Resource):
    @api.doc('list_of_brands')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @admin_token_required
    @api.marshal_list_with(brand, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_brands()
    
    @api.expect(post_brand, validate=True)
    @api.response(201, 'Brand successfully created.')
    @api.doc('create a new brand')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @admin_token_required
    def post(self):
        """Creates a new Brand """
        data = request.json
        return save_new_brand(data=data)
    

@api.route('/<id>')
@api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
@api.param('id', 'Brand identifier')
@api.response(404, 'Brand not found.')
class Brand(Resource):
    @api.doc('get a brand')
    @api.marshal_with(brand)
    def get(self, id):
        """get a brand given its identifier"""
        _brand = get_a_brand(id)
        if not _brand:
            api.abort(404)
        else:
            return _brand, 200
        
    @api.doc('update a brand')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @api.expect(put_brand, validate=True)
    @api.response(200, 'Brand successfully updated.')
    @api.response(404, 'Brand not found.')
    @admin_token_required
    def put(self, id):
        """Brand a Product """
        _brand = get_a_brand(id)
        if not _brand:
            api.abort(404)
        else:
            data = request.json
            data['id'] = id
            return update_brand(data=data)
        
    @api.doc('delete a brand')
    @api.response(204, 'Brand successfully deleted.')
    @api.response(404, 'Brand not found.')
    @api.response(400, 'Brand can\'t be deleted because ofe existing foreign key mappings.')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @admin_token_required
    def delete(self, id):
        """Delete a brand given its identifier"""
        _brand = get_a_brand(id)
        if not _brand:
            api.abort(404)
        else:
            return delete_brand_method(_brand.id)
