import click
from flask import Flask, render_template, request, jsonify
from flask_restful import Api
from flask_cors import CORS, cross_origin
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from resources.user import UserRegister, User
from resources.role import Role

from security import authenticate, identity

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

POSTGRES_URL="127.0.0.1:5432"
POSTGRES_USER="postgres"
POSTGRES_PW="password123"
POSTGRES_DB="cosin-flask"

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret2'  # Change this!
jwt = JWTManager(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'secret'
cors = CORS(app, supports_credentials = True)

api = Api(app)

# jwt = JWT(app, authenticate, identity) # /auth

# move to run.py when deploying to heroku
@app.before_first_request
def create_tables():
  db.create_all()

@app.route('/')
def home():
  return render_template('index.html')

# FLASK_APP=server.py flask resetdb
@app.cli.command('resetdb')
def resetdb_command():
    """Destroys and creates the database + tables."""
    from db import db
    from models.user import UserModel
    from models.role import RoleModel
    db.init_app(app)

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

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"message": "Missing email parameter"}), 400
    if not password:
        return jsonify({"message": "Missing password parameter"}), 400

    user = authenticate(email, password)

    if not user:
        return jsonify({"message": "Bad email or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity = email)
    return jsonify(access_token = access_token, user = user.json()), 200

api.add_resource(UserRegister, '/register')
api.add_resource(Role, '/role/<string:name>')
api.add_resource(User, '/user/<string:email>')

if __name__ == '__main__':
  from db import db
  db.init_app(app)

  app.run(port = 5000, debug = True)