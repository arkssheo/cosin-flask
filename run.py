from server import app
from db import db

db.init_app(app)

@app.before_first_request
def create_tables():
  db.create_all()

# FLASK_APP=run.py flask resetdb
@app.cli.command('resetdb')
def resetdb_command():
    """Destroys and creates the database + tables."""
    from models.user import UserModel
    from models.role import RoleModel
    import os

    from sqlalchemy_utils import database_exists, create_database, drop_database

    DB_URL = os.environ.get('DATABASE_URL', 'sqlite:///data.db')

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
