from datetime import date, datetime
from .. import db
from .base import BaseModel
from .store import store_brand_association


class Brand(BaseModel):
    """
    Model for the brands table
    """
    __tablename__ = "brands"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    products = db.relationship('Product', backref='brands', lazy=True)
    stores = db.relationship("Store", secondary=store_brand_association, back_populates="brands")
    
    def __repr__(self):
        return "<Brand '{}'>".format(self.id)
    
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