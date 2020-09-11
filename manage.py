import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint
from app.main import create_app, db
from app.main.model import user, blacklist, role, store, item, product, brand, inventory

app = create_app(os.getenv('DEPLOYMENT_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()


@manager.command
def initiate_dbs():
    from app.main.model.store import Store
    from app.main.model.user import User
    from app.main.model.role import Role, RoleType
    from app.main import db

    store = Store(name="ABC Retail 1", email="retail1@abc.com")
    db.session.add(store)
    db.session.commit()

    role = Role(name=RoleType.ADMIN, store_id=store.id)
    db.session.add(role)
    db.session.commit()

    user = User(email="admin1@abc.com", password="abc123")
    user.roles.append(role)
    db.session.add(user)
    db.session.commit()


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
