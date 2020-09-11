from datetime import date, datetime
from .. import db
from .base import BaseModel


store_brand_association = db.Table('store_brand_association',
    db.Column('store_id', db.Integer, db.ForeignKey('stores.id')),
    db.Column('brand_id', db.Integer, db.ForeignKey('brands.id'))
)


class Store(BaseModel):
    """
    Model for the stores table
    """
    __tablename__ = "stores"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    inventory = db.relationship('Inventory', backref='stores', lazy=True)
    roles = db.relationship('Role', backref='stores', lazy=True)
    dp = db.Column(db.String(
        120), default="https://ethos-photos.s3.ap-south-1.amazonaws.com/default_dp.png")
    brands = db.relationship("Brand", secondary=store_brand_association)
    
    def __repr__(self):
        return "<Store '{}'>".format(self.id)
    
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
            else:
                as_json[column] = value
        return as_json