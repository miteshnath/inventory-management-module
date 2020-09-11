from datetime import date, datetime
from .. import db
from .base import BaseModel


class Item(BaseModel):
    """
    Model for the users table
    """
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(50), nullable=False)
    is_damaged = db.Column(db.Boolean, default=False)
    is_sold = db.Column(db.Boolean, default=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    def __repr__(self):
        return "<Item '{}'>".format(self.serial_number)
    
    def _to_dict(self): 
        as_json = {}
        for column, value in self.__dict__.items():
            if column == '_sa_instance_state':
                continue
            elif isinstance(value, (datetime, date)):
                as_json[column] = value.isoformat()
            else:
                as_json[column] = value
        return as_json