from . import db
from app import app
from flask.ext.sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class User_info(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(150))
  email = db.Column(db.String(80), unique=True)
  password_hash = db.Column(db.String(255))
  
  def __init__(self, name, email, password): 
    self.name = name
    self.email = email.lower()
    self.hash_password(password)
    
  def hash_password(self, password):
      self.password_hash = pwd_context.encrypt(password)

  def verify_password(self, password):
      return pwd_context.verify(password, self.password_hash)
      
  def generate_auth_token(self, expiration = 600):
      s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
      return s.dumps({ u'id':  self.id})

  @staticmethod
  def verify_auth_token(token):
      s = Serializer(app.config['SECRET_KEY'])
      try:
          data = s.loads(token)
      except SignatureExpired:
          return None # valid token, but expired
      except BadSignature:
          return None # invalid token
      user = User_info.query.get(data['id'])
      return user

  def __repr__(self):
    return '<User %r>' % self.id
    
class Wishes(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(180))
  description = db.Column(db.Text)
  thumbnail = db.Column(db.String(255))
  user = db.Column(db.Integer, db.ForeignKey("user_info.id"))
  url = db.Column(db.String(255))
  
  def __init__(self, title, description, thumbnail, user, url): 
    self.title = title
    self.description = description
    self.thumbnail = thumbnail
    self.user = user
    self.url = url
    
  def __repr__(self):
    return '<Wish %r>' % self.title