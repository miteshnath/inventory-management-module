from datetime import date, datetime
from .. import db
from .base import BaseModel


class Inventory(BaseModel):
    """
    Model for the inventories table
    """
    __tablename__ = "inventories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    products = db.relationship('Product', backref='inventories', lazy=True)
    
    def __repr__(self):
        return "<Inventory '{}'>".format(self.id)
    
    def _to_dict(self): 
        as_json = {}
        for column, value in self.__dict__.items():
            if column == '_sa_instance_state':
                continue
            elif column == "products":
                _products = []
                if self.products:
                    _products = [_pro._to_dict() for _pro in self.products]
                as_json['products'] = _products
            elif isinstance(value, (datetime, date)):
                as_json[column] = value.isoformat()
            else:
                as_json[column] = value
        return as_json