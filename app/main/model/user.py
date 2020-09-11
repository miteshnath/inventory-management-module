from datetime import date, datetime, timedelta
from .. import db, flask_bcrypt

from app.main.model.blacklist import BlacklistToken
from ..config import key
from .base import BaseModel
from .role import role_user_association
import jwt


class User(BaseModel):
    """ User Model for storing user related details """
    __tablename__ = "users"


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    roles = db.relationship("Role", secondary=role_user_association, back_populates="users")
    dp = db.Column(db.String(
        120), default="https://ethos-photos.s3.ap-south-1.amazonaws.com/default_dp.png")

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1, seconds=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<User '{}'>".format(self.email)
    
    def _to_dict(self): 
        as_json = {}
        for column, value in self.__dict__.items():
            if column == '_sa_instance_state':
                continue
            elif column == "roles":
                _roles = []
                if self.roles:
                    _roles = [_role._to_dict() for _role in self.roles]
                as_json['roles'] = _roles 
            elif isinstance(value, (datetime, date)):
                as_json[column] = value.isoformat()
            elif column == "roles":
                import pdb; pdb.set_trace()
            else:
                as_json[column] = value
        return as_json