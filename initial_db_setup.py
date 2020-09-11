from app.main.model.store import Store
from app.main.model.user import User
from app.main.model.role import Role, RoleType
from app.main import db

store = Store(name="ABC Retail 1", email="retail1@abc.com")
db.session.add(store)
db.session.commit()

role = Role(name=RoleType.ADMIN, store_id=store.id)
role_work = Role(name=RoleType.WORKER, store_id=store.id)
db.session.add(role)
db.session.add(role_work)
db.session.commit()

user = User(email="admin1@abc.com", password="abc123")
user1 = User(email="admin2@abc.com", password="abc123")
user.roles.append(role)
user1.roles.append(role_work)
db.session.add(user)
db.session.add(user1)
db.session.commit()
