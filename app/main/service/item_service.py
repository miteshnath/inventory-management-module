import uuid
import datetime

from app.main import db
from ..model.item import Item
from .user_service import save_changes, delete_record



def get_all_items():
    return Item.query.all()


def get_an_item(id):
    return Item.query.filter_by(id=id).first()


def save_new_item(data):
    item = Item.query.filter_by(serial_number=data['serial_number']).first()
    if not item:
        new_item = Item(
            serial_number=data.get('serial_number', ''),
            is_damaged=data.get('is_damaged', False),
            is_sold=data.get('is_sold', False),
            product_id=data['product_id']
        )
        save_changes(new_item)
        response_object = {
            'status': 'success',
            'message': 'Item successfully created'
        }
        response_object['item'] = get_an_item(new_item.id)._to_dict()
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Brand with this name already exists',
        }
        return response_object, 400
    
    
def update_item(data):
    item = Item.query.filter_by(id=data['id']).first()
    item.serial_number = data.get('serial_number') if data.get('serial_number') is not None else item.serial_number
    item.is_damaged = data.get('is_damaged') if data.get('is_damaged') is not None else item.is_damaged
    item.is_sold = data.get('is_sold') if data.get('is_sold') is not None else item.is_sold
    save_changes(None, is_update=True)
    response_object = {
        'status': 'success',
        'message': 'Item successfully created'
    }
    response_object['item'] = get_an_item(item.id)._to_dict()
    return response_object, 200


def delete_item_method(id):
    _item = Item.query.filter_by(id=id).one()
    return delete_record(_item)
    