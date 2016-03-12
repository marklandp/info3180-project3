from flask.ext.wtf import Form
from wtforms.fields import TextField, IntegerField, RadioField, FileField
#other fields..PasswordField
from wtforms.validators import Required

class NewProfileForm(Form):
  username = TextField('Username', validators=[Required()])
#   image = #file upload field
#   image = TextField('Image', validators=[Required()])
  image = FileField('Image', validators=[Required()])
  fname = TextField('First Name', validators=[Required()])
  lname = TextField('Last Name', validators=[Required()])
  age = IntegerField('Age', validators=[Required()])
  sex = RadioField('Sex', choices=[('Male','Male'),('Female','Female')], validators=[Required()])