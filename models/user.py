from db import db
import hashlib

class UserModel(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key = True)
  first_name = db.Column(db.String(150))
  last_name = db.Column(db.String(150))
  email = db.Column(db.String(80))
  password = db.Column(db.String(80))

  def __init__(self, email, password):
    self.email = email
    self.password = self.hash_password(password)

  @classmethod
  def hash_password(cls, password):
    bytes_object = bytes(password, encoding = 'utf-8')
    hash_object = hashlib.sha1(bytes_object)
    return hash_object.hexdigest()

  @classmethod
  def find_by_email(cls, email):
    return cls.query.filter_by(email = email).first()

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id = _id).first()

  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

