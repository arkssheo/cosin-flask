from models.user import UserModel

def authenticate(email, password):
  user = UserModel.find_by_email(email)
  hashed_password = UserModel.hash_password(password)
  if user and hashed_password == user.password:
    return user

def identity(payload):
  user_id = payload['identity']
  return UserModel.find_by_id(user_id)