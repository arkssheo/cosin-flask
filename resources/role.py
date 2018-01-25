from flask_restful import Resource, reqparse
from models.role import RoleModel

class Role(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('is_admin', type = bool)

  def post(self, name):
    data = Role.parser.parse_args()
    # role_name = data['role_name']

    if RoleModel.find_by_name(name):
      return {'message', 'A role with this name already exists'}, 400

    is_admin = data['is_admin']

    if is_admin is None:
      is_admin = False

    role = RoleModel(name, is_admin)

    try:
      role.save()
    except:
      return {'message': 'Error saving the role'}, 500

    return role.json(), 201