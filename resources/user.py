from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('email',
    type = str,
    required = True,
    help = 'email is required'
  )
  parser.add_argument('password',
    type = str,
    required = True,
    help = 'password is required'
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
