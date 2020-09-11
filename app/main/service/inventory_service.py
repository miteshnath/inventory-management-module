import uuid
import datetime

from app.main import db
from ..model.inventory import Inventory
from .product_service import get_a_product
from .user_service import save_changes, delete_record



def get_all_inventories():
    return Inventory.query.all()


def get_an_inventory(id):
    return Inventory.query.filter_by(id=id).first()


def save_new_inventory(data):
    inventory = Inventory.query.filter_by(name=data['name'], store_id=data['store_id']).first()
    if not inventory:
        new_invent = Inventory(
            name=data['name'],
            store_id=data['store_id']
        )
        for id in data.get('products', []):
            new_invent.append(get_a_product(id))
        save_changes(new_invent)
        response_object = {
            'status': 'success',
            'message': 'Inventory successfully created'
        }
        response_object['inventory'] = get_an_inventory(new_invent.id)._to_dict()
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Inventory with this name already exists',
        }
        return response_object, 400
    

def save_new_inventory(data):
    inventory = Inventory.query.filter_by(name=data['name'], store_id=data['store_id']).first()
    if not inventory:
        new_invent = Inventory(
            name=data['name'],
            store_id=data['store_id']
        )
        for _id in data.get('products', []):
            new_invent.products.append(get_a_product(_id))
        save_changes(update=True)
        response_object = {
            'status': 'success',
            'message': 'Inventory successfully created'
        }
        response_object['inventory'] = get_an_inventory(new_invent.id)._to_dict()
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Inventory with this name already exists',
        }
        return response_object, 400


def update_inventory(data):
    inventory = Inventory.query.filter_by(id=data['id'], store_id=data['store_id']).first()
    inventory.name = data.get('name') if data.get('name') is not None else inventory.name
    for _id in data.get('products', []):
        _prod = get_a_product(_id)
        if _prod is not None:
            inventory.products.append(_prod)
    save_changes(None, is_update=True)
    response_object = {
        'status': 'success',
        'message': 'Inventory successfully created'
    }
    response_object['inventory'] = get_an_inventory(inventory.id)._to_dict()
    return response_object, 200


def delete_inventory_method(id):
    _invent = Inventory.query.filter_by(id=id).one()
    return delete_record(_invent)
    