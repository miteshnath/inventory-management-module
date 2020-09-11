import uuid
import datetime

from app.main import db
from ..model.product import Product
from .user_service import save_changes, delete_record
from .item_service import get_an_item



def get_all_products():
    return Product.query.all()


def get_a_product(id):
    return Product.query.filter_by(id=id).first()


def save_new_product(data):
    product = Product.query.filter_by(name=data['name'],
                                       inventory_id=data['inventory_id'],
                                        brand_id=data['brand_id']).first()
    if not product:
        new_product = Product(
            name=data['name'],
            inventory_id=data['inventory_id'],
            dp=data.get('dp', ''),
            brand_id=data['brand_id'],
            max_quantity=data.get('max_quantity', 10),
            quantity_available = data.get('quantity_available', 0)
        )
        for id in data.get('items', []):
            new_product.append(get_an_item(id))
        save_changes(new_product)
        response_object = {
            'status': 'success',
            'message': 'Product successfully created'
        }
        response_object['product'] = get_a_product(new_product.id)._to_dict()
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Duplicate product'}
        return response_object, 400
    

def update_product(data):
    _prod = Product.query.filter_by(id=data['id'], brand_id=data['brand_id']).first()
    _prod.name = data.get('name') if data.get('name') is not None else _prod.name
    _prod.max_quantity = data['max_quantity'] if data.get('max_quantity') is not None else _prod.max_quantity
    _prod.quantity_available = data['quantity_available'] if data.get('quantity_available') is not None else _prod.quantity_available
    for _id in data.get('items', []):
        _item = get_an_item(_id)
        if _item is not None:
            _prod.items.append(_item)
    save_changes(None, is_update=True)
    response_object = {
        'status': 'success',
        'message': 'Product successfully created'
    }
    response_object['product'] = get_a_product(_prod.id)._to_dict()
    return response_object, 200


def delete_product_method(id):
    _prod = Product.query.filter_by(id=id).one()
    return delete_record(_prod)