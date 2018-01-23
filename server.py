from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT

from resources.user import UserRegister, User
from resources.role import Role

from security import authenticate, identity

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
app.secret_key = 'secret'

api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

# move to run.py when deploying to heroku
@app.before_first_request
def create_tables():
  db.create_all()

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