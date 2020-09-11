from datetime import date, datetime

from .. import db
from .base import BaseModel
import enum


role_user_association = db.Table('role_user_association',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)


class RoleType(enum.Enum):
    ADMIN = "admin"
    WORKER = "worker"


class Role(BaseModel):
    """
    Model for the roles table
    """
    __tablename__ = "roles"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(RoleType))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    users = db.relationship("User", secondary=role_user_association, back_populates="roles")
    
    def __repr__(self):
        return "<Role '{}'>".format(self.id)
    
    def _to_dict(self): 
        as_json = {}
        for column, value in self.__dict__.items():
            if column == '_sa_instance_state':
                continue
            elif column == "users":
                _users = []
                if self.users:
                    _users = [_user._to_dict() for _user in self.users]
                as_json['users'] = _users 
            elif isinstance(value, (datetime, date)):
                as_json[column] = value.isoformat()
            else:
                as_json[column] = value
        return as_json