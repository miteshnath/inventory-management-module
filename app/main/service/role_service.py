import uuid
import json
import datetime

from app.main import db
from ..model.role import Role
from .user_service import save_changes, get_a_user



def get_all_roles():
    return Role.query.all()


def get_a_role(id):
    return Role.query.filter_by(id=id).first()


def save_new_role(data):
    name = data.get('name').upper()
    role = Role.query.filter_by(name=name, store_id=data['store_id']).first()
    if not role:        
        new_role = Role(
            name=name,
            store_id=data['store_id'],
        )
        for id in data.get('users', []):
            new_role.append(get_a_user(id))
        save_changes(new_role)
        response_object = {
            'status': 'success',
            'message': 'Role successfully created'
        }
        response_object['role'] = get_a_role(new_role.id)._to_dict()
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Role with this name already exists for this store',
        }
        return response_object, 400