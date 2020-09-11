from flask_restx import Namespace, fields
from ..model.role import RoleType


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })
    
    
class RoleDto:
    api = Namespace('role', description='role related operations')
    role = api.model('role', {
        'id': fields.Integer(required=False, description='role id'),
        'name': fields.String(description='role type options', enum=[k.lower() for k, v in RoleType.__members__.items()]),
        'store_id': fields.Integer(description='parent store id', required=True)
    })


class ItemDto:
    api = Namespace('item', description='item related operations')
    item = api.model('item', {
        'id': fields.Integer(required=False, description='item id'),
        'serial_number': fields.String(description='product name'),
        'is_damaged': fields.Boolean(required=False),
        'is_sold': fields.Boolean(required=False),
        'product_id': fields.Integer(required=True, description='id of product item belongs to')
    })
    post_item = api.model('item', {
        'serial_number': fields.String(description='product name'),
        'is_damaged': fields.Boolean(default=False),
        'is_sold': fields.Boolean(default=False),
        'product_id': fields.Integer(required=True, description='id of product item belongs to')
    })
    put_item = api.model('item', {
        'serial_number': fields.String(required=False, description='product name'),
        'is_damaged': fields.Boolean(required=False),
        'is_sold': fields.Boolean(required=False)
    })

  
class ProductDto:
    api = Namespace('product', description='prodcut related operations')
    product = api.model('product', {
        'id': fields.Integer(required=False, description='product id'),
        'name': fields.String(description='product name'),
        'dp': fields.String(required=False, description='store display image'),
        'inventory_id': fields.Integer(required=True, description='id of inventory product belongs to'),
        'brand_id': fields.Integer(required=True, description='id of brand product belongs to'),
        'quantity_available': fields.Integer(required=True, description='current available quantity'),
        'max_quantity': fields.Integer(required=True, description='max quantity in this store inventory'),
        'items': fields.List(fields.Nested(ItemDto.item))
    })
    post_product = api.model('product', {
        'name': fields.String(description='product name'),
        'inventory_id': fields.Integer(required=True, description='id of inventory product belongs to'),
        'brand_id': fields.Integer(required=True, description='id of brand product belongs to'),
        'quantity_available': fields.Integer(required=True, description='current available quantity'),
        'max_quantity': fields.Integer(required=True, description='max quantity in this store inventory'),
        'items': fields.List(fields.Nested(ItemDto.item))
    })
    put_product = api.model('product', {
        'name': fields.String(required=False, description='product name'),
        'quantity_available': fields.Integer(required=False, description='current available quantity'),
        'max_quantity': fields.Integer(required=False, description='max quantity in this store inventory'),
        'items': fields.List(fields.Integer(description='item identifier'))
    })
    
class BrandDto:
    api = Namespace('brand', description='brand related operations')
    brand = api.model('brand', {
        'id': fields.Integer(required=False, description='brand id'),
        'name': fields.String(required=True, description='brand name'),
        'products': fields.List(fields.Nested(ProductDto.product))
    })
    post_brand = api.model('brand', {
        'name': fields.String(required=True, description='brand name'),
        'products': fields.List(fields.Integer(description='Product identifier')),    
    })
    put_brand = api.model('brand', {
        'name': fields.String(required=False, description='brand name'),
        'products': fields.List(fields.Integer(description='Product identifier')),    
    })
                      
                      
class InventoryDto:
    api = Namespace('inventory', description='inventory related operations')
    inventory = api.model('inventory', {
        'id': fields.Integer(required=False, description='inventory id'),
        'name': fields.String(required=True, description='inventory name'),
        'store_id': fields.Integer(required=True, description='store to which inventory belongs'),
        'products': fields.List(fields.Nested(ProductDto.product))
    })
    post_inventory = api.model('inventory', {
        'store_id': fields.Integer(required=True, description='store to which inventory belongs'),
        'name': fields.String(required=True, description='brand name'),
        'products': fields.List(fields.Integer(description="Product identifiers"))
    })
    put_inventory = api.model('inventory', {
        'name': fields.String(required=False, description='brand name'),
        'products': fields.List(fields.Integer(description="Product identifiers"))
    })

    
class StoreDto:
    api = Namespace('store', description='store related operations')
    store = api.model('store', {
        'id': fields.Integer(required=False, description='role id'),
        'name': fields.String(description='store name'),
        'email': fields.String(required=True, description='store email'),
        'dp': fields.String(required=False, description='store display image'),
        'roles': fields.List(fields.Nested(RoleDto.role))
    })


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='email address'),
        'roles': fields.List(fields.Nested(RoleDto.role))
    })
