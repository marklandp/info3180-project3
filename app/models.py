from . import db
class User_info(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)
  userid = db.Column(db.Integer, unique=True)
  image = db.Column(db.String(200))
  email = db.Column(db.String(40))
  password = db.Column(db.String(100))
  age = db.Column(db.Integer)
  sex = db.Column(db.String(8))
  datejoined = db.Column(db.DateTime)
  
  def __init__(self, username, userid, image, email, password, age, sex, date): 
    self.username = username
    self.userid = userid
    self.image = image
    self.email = email
    self.password = password
    self.age = age
    self.sex = sex
    self.datejoined = date

  def __repr__(self):
    return '<User %r>' % self.username