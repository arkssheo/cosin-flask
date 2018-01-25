from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.user import UserModel

userparser = reqparse.RequestParser()
userparser.add_argument('email',
  type = str,
  required = True,
  help = 'email is required'
)

class User(Resource):
  parser = userparser.copy()

  #@jwt_required()
  def get(self, email):
    user = UserModel.find_by_email(email)
    if user:
      return user.json()
    return {'message': 'User with email {} not found'.format(email)}, 404

class UserRegister(Resource):
  parser = userparser.copy()
  parser.add_argument('password',
    type = str,
    required = True,
    help = 'password is required'
  )
  parser.add_argument('role_id', 
    type = int,
    required = True,
    help = 'role_id is required'
  )

  def post(self):
    data = UserRegister.parser.parse_args()

    if UserModel.find_by_email(data['email']):
      return {'message': 'An user with this email already exists'}, 400

    user = UserModel(**data)
    user.save()

    return {'message': 'User created successfully!'}, 201

  # def get(self):
  #   data = User.parser.parse_args()

  #   user = UserModel.find_by_email(data['email'])
  #   if user:
  #     return user.json()
  #   return {'message': 'User not found'}
