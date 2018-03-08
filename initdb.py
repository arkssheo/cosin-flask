"""Destroys and creates the database + tables."""
from models.user import UserModel
from models.role import RoleModel
from db import db
from sqlalchemy_utils import database_exists, create_database, drop_database

if database_exists(DB_URL):
    print('Deleting database.')
    drop_database(DB_URL)
if not database_exists(DB_URL):
    print('Creating database.')
    create_database(DB_URL)

print('Creating tables.')
db.create_all()

print('Adding role: Admin')
admin_role = RoleModel('Administrador', True)
db.session.add(admin_role)
db.session.commit()

print('Adding Admin user')
admin = UserModel('admin@cosin.com.mx', 'adminpassword', '1')
db.session.add(admin)
db.session.commit()

print('Done!')