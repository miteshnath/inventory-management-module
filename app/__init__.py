from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.brand_controller import api as brand_ns
from .main.controller.item_controller import api as item_ns
from .main.controller.inventory_controller import api as inventory_ns
from .main.controller.product_controller import api as product_ns
from .main.controller.role_controller import api as role_ns
from .main.controller.store_controller import api as store_ns

blueprint = Blueprint('api', __name__)

authorizations = {
    'basic': {
        'type': 'basic',
        'in': 'headers',
        'name': 'Authorization'
    }
}

api = Api(blueprint,
          title='Inventory Management System',
          version='1.0',
          authorizations=authorizations,
          security='basic',
          description='inventory management system in flask restplus as a web service'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(brand_ns, path='/brand')
api.add_namespace(item_ns, path='/item')
api.add_namespace(inventory_ns, path='/inventory')
api.add_namespace(product_ns, path='/product')
api.add_namespace(role_ns, path='/role')
api.add_namespace(store_ns, path='/store')