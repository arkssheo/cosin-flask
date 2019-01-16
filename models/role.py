from db import db

class RoleModel(db.Model):
  __tablename__ = 'roles'

  id = db.Column(db.Integer, primary_key = True)
  role_name = db.Column(db.String(150))
  is_admin = db.Column(db.Boolean)

  def __init__(self, role_name, is_admin = False):
    self.role_name = role_name
    self.is_admin = is_admin

  def json(self):
    return {'_id': self.id, 'name': self.role_name, 'is_admin': self.is_admin}

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id = _id).first()

  @classmethod
  def find_by_name(cls, role_name):
    return cls.query.filter_by(role_name = role_name).first()

  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
