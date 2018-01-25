from flask import Flask, render_template, request
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS

from resources.user import UserRegister, User
from resources.role import Role

from security import authenticate, identity

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
app.secret_key = 'secret'
#cors = CORS(app, resources={r"*": {"origins": "*"}})

api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

# move to run.py when deploying to heroku
@app.before_first_request
def create_tables():
  db.create_all()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response

@app.route('/')
def home():
  return render_template('index.html')

api.add_resource(UserRegister, '/register')
api.add_resource(Role, '/role/<string:name>')
api.add_resource(User, '/user/<string:email>')

if __name__ == '__main__':
  from db import db
  db.init_app(app)

  app.run(port = 5000, debug = True)