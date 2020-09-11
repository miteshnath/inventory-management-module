import uuid
import datetime

from app.main import db
from ..model.brand import Brand
from .product_service import get_a_product
from .user_service import save_changes, delete_record



def get_all_brands():
    return Brand.query.all()


def get_a_brand(id):
    return Brand.query.filter_by(id=id).first()


def save_new_brand(data):
    brand = Brand.query.filter_by(name=data['name']).first()
    if not brand:
        new_brand = Brand(
            name=data['name']
        )
        for id in data.get('products', []):
            new_brand.append(get_a_product(id))
        save_changes(new_brand)
        response_object = {
            'status': 'success',
            'message': 'Brand successfully created'
        }
        response_object['brand'] = get_a_brand(new_brand.id)._to_dict()
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Brand with this name already exists',
        }
        return response_object, 400
    


def update_brand(data):
    brand = Brand.query.filter_by(id=data['id']).first()
    brand.name = data.get('name') if data.get('name') is not None else brand.name
    for _id in data.get('products', []):
        _prod = get_a_product(_id)
        if _prod is not None:
            brand.products.append(_prod)
    save_changes(None, is_update=True)
    response_object = {
        'status': 'success',
        'message': 'Brand successfully created'
    }
    response_object['brand'] = get_a_brand(brand.id)._to_dict()
    return response_object, 200


def delete_brand_method(id):
    _invent = Brand.query.filter_by(id=id).one()
    return delete_record(_invent)
    