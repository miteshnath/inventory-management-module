from datetime import date, datetime
from .. import db
from .base import BaseModel


class Product(BaseModel):
    """
    Model for the products table
    """
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    dp = db.Column(db.String(
        120), default="https://ethos-photos.s3.ap-south-1.amazonaws.com/default_dp.png")
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventories.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    items = db.relationship('Item', backref='products', lazy=True)
    quantity_available = db.Column(db.Integer, default=0)
    max_quantity = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return "<Product '{}'>".format(self.id)
    
    def _to_dict(self): 
        as_json = {}
        for column, value in self.__dict__.items():
            if column == '_sa_instance_state':
                continue
            elif column == "items":
                _items = []
                if self.items:
                    _items = [_item._to_dict() for _item in self.items]
                as_json['items'] = _items 
            elif isinstance(value, (datetime, date)):
                as_json[column] = value.isoformat()
            else:
                as_json[column] = value
        return as_json