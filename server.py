import click, os
from flask import Flask, render_template, request, jsonify, redirect, url_for, abort
from flask_restful import Api
from flask_cors import CORS, cross_origin
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from resources.user import UserRegister, User
from resources.role import Role

from models.user import UserModel
from models.role import RoleModel

from security import authenticate, identity

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# POSTGRES_URL="127.0.0.1:5432"
# POSTGRES_USER="postgres"
# POSTGRES_PW="password123"
# POSTGRES_DB="cosin-flask"

# DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
#     user = POSTGRES_USER,
#     pw = POSTGRES_PW,
#     url = POSTGRES_URL,
#     db = POSTGRES_DB)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret2'  # Change this!
jwt = JWTManager(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'secret'
cors = CORS(app, supports_credentials = True)

api = Api(app)

# jwt = JWT(app, authenticate, identity) # /auth

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/admin')
def admin_cp():
    users = UserModel.query.all()
    roles = RoleModel.query.all()
    return render_template('admin_cp.html', users=users, roles=roles)


@app.route('/admin/user', methods=['GET', 'POST'])
def admin_user():
    if request.method == 'GET':
        email = request.args.get('email')
        user = UserModel.find_by_email(email)
        return render_template('user_management.html', user=user)
    elif request.method == 'POST':
        email = request.args.get('email')
        password = request.args.get('password')
        user = UserModel.find_by_email(email)
        user.reset_password(password)
        return render_template('user_management.html', user=user, message='Password Changed!')

@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        role_id = request.form.get('role_id', None)
        if email is None or password is None or role_id is None:
            print('Got: %s %s %s' % email, password, role_id)
            return abort(404)
        user = UserModel(email=email, password=password, role_id=role_id)
        user.save()
        return redirect( url_for('admin_cp') )
    else:
        roles = RoleModel.query.all()
        return render_template('register.html', roles=roles)

@app.route('/admin/delete_user', methods=['POST'])
def admin_delete_user():
    user = UserModel.find_by_email(request.form.get('email', ''))
    if user is not None:
        user.delete()
        return redirect( url_for('admin_cp') )

@app.route('/admin/role', methods=['GET', 'POST'])
def admin_role():
    if request.method == 'POST':
        pass
    else:
        role_name = request.args.get('role_name')
        role = RoleModel.find_by_name(role_name)
        return render_template('role_mgmt.html', role=role)

@app.route('/admin/new_role', methods=['GET', 'POST'])
def admin_new_role():
    if request.method == 'POST':
        is_admin = False if request.form.get('is_admin', None) is None else True
        role_name = request.form.get('role_name', None)

        if role_name is None:
            return render_template('new_role.html')

        role = RoleModel(role_name=role_name, is_admin=is_admin)
        role.save()
        return redirect( url_for('admin_cp') )
    else:
        return render_template('new_role.html')

@app.route('/admin/delete_role', methods=['POST'])
def admin_delete_role():
    role = RoleModel.find_by_name(request.form.get('role_name', ''))
    if role is not None:
        role.delete()
    else:
        print('[DELETE ROLE] Could not delete role with name: %s' % request.form.get('role_name'))

    return redirect( url_for('admin_cp') )


""" API Methods """

@app.route('/api/login', methods=['POST'])
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

@app.route('/api/roles', methods=['GET'])
def api_roles():
    roles = RoleModel.query.all()
    return jsonify({"roles": [role.json() for role in roles]}), 200

@app.route('/api/create_user', methods=['POST'])
def api_create_user():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    role_id = request.json.get('roleId', None)
    if email is None or password is None or role_id is None:
        print('Error creating user, email(%s), password(%s), role_id(%s)' % (email, password, role_id))
        return jsonify({"message": "Missing parameters, need email, password and role_id"}), 400

    role = RoleModel.query.get(role_id)
    if role is None:
        return jsonify({"message": "Invalid role id"}), 400

    user = UserModel(email=email, password=password, role_id=role_id)
    user.save()
    return jsonify({"message": "User created successfully!"}), 201

api.add_resource(UserRegister, '/register')
api.add_resource(Role, '/role/<string:name>')
api.add_resource(User, '/user/<string:email>')

if __name__ == '__main__':
  from db import db
  db.init_app(app)

  app.run(port = 5000, debug = True)
