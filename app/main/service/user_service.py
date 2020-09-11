import uuid
import datetime
from sqlalchemy.exc import IntegrityError
from app.main import db
from ..model.user import User


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            email=data.get('email'),
            password=data.get('password')
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(id):
    return User.query.filter_by(id=id).first()


def generate_token(user):
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def save_changes(data, is_update=False):
    try:
        if data is not None and not is_update:
            db.session.add(data)    
    
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception
    
def delete_record(data):
    try:
        db.session.delete(data)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'record successfully deleted'
        }
        return response_object, 204
    
    except IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'cannot delete this record! existing foreign key mappings'
        }
        return response_object, 400