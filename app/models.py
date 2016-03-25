from . import db
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

class User_info(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  fname = db.Column(db.String(80))
  lname = db.Column(db.String(80))
  image = db.Column(db.String(200))
  email = db.Column(db.String(50), unique=True)
  password = db.Column(db.String(100))
  age = db.Column(db.Integer)
  sex = db.Column(db.String(8))
  datejoined = db.Column(db.DateTime)
  
  def __init__(self, fname, lname, image, email, password, age, sex, date): 
    self.fname = fname
    self.lname = lname
    self.image = image
    self.email = email.lower()
    self.age = age
    self.sex = sex
    self.datejoined = date
    self.set_password(password)
     
  def set_password(self, password):
    self.password = generate_password_hash(password)
   
  def check_password(self, password):
    return check_password_hash(self.password, password)
    
  def is_authenticated(self):
      return True
 
  def is_active(self):
      return True
 
  def is_anonymous(self):
      return False
 
  def get_id(self):
      return unicode(self.id)

  def __repr__(self):
    return '<User %r>' % self.username
    
class Wishes(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(150))
  description = db.Column(db.String(200))
  url = db.Column(db.String(200))
  user = db.Column(db.String(50), db.ForeignKey("user_info.email"))
  
  def __init__(self, title, description, url, user): 
    self.title = title
    self.description = description
    self.url = url
    self.user = user
    
  def __repr__(self):
    return '<Wish %r>' % self.title
  