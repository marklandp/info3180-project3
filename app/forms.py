from flask.ext.wtf import Form
from wtforms.fields import TextField, IntegerField, SelectField, FileField, PasswordField
from wtforms.validators import Required, Length, EqualTo, ValidationError, Email, NumberRange
from app.models import User_info
from app import db

class Unique(object):
    """ validator that checks field uniqueness """
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = u'Username already exists'
        self.message = message

    def __call__(self, form, field):         
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)

class RegistrationForm(Form):
  username = TextField('Username', validators=[Required(message="Must choose a username"), Length(min=2, max=15), Unique(User_info, User_info.username)])
  email = TextField('Email Address', validators=[Length(min=6, max=35), Required("Required"), Email()])
  confirme = TextField('Confirm Email', validators=[Required(message="Required"), EqualTo('email', message='email doesn\'t match original')])
  password = PasswordField('New Password', validators=[Required("Required"), Length(min=8, max=100)])
  confirmp = PasswordField('Confirm Password', validators=[Required(message="Required"),EqualTo('password', message='Password mismatch')])
  image = FileField('Image', validators=[Required(message="Must upload an image")])
  age = IntegerField('Age', validators=[Required(message="Required"), NumberRange(min=10,max=85, message="Only 10 - 85 year olds")])
  sex = SelectField('Sex', choices=[('Male','Boy'),('Female','Girl')], validators=[Required(message="Required")])
  