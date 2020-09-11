import uuid
import datetime
import json

from flask import jsonify

from app.main import db
from ..model.store import Store
from .user_service import save_changes



def get_all_stores():
    return Store.query.all()


def get_a_store(id):
    return Store.query.filter_by(id=id).first()


def save_new_store(data):
    store = Store.query.filter_by(email=data['email']).first()
    if not store:
        new_store = Store(
            email=data['email'],
        )
        save_changes(new_store)
        response_object = {
            'status': 'success',
            'message': 'Store successfully created'
        }
        response_object['store'] = get_a_store(new_store.id)._to_dict()
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Store with this email already exists',
        }
        return response_object, 400
