"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

from app import app
from flask import render_template, request, redirect, url_for, flash
from app import db
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from app.models import User_info
from flask import jsonify, session
from datetime import *
from .forms import RegistrationForm
import json
from flask import Response
from werkzeug.utils import secure_filename
from sqlalchemy.sql.expression import func
import os
import time


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


def timeinfo():
    return datetime.now()
    
@app.route('/register/', methods=['POST', 'GET'])
def register():
  """Render the profile page"""
  form = RegistrationForm()
  if form.validate_on_submit():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    age = int(request.form['age'])
    sex = request.form['sex']
    photo = request.files['image']
    imagename = username + '_' + secure_filename(photo.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], imagename)
    photo.save(file_path)
    get_id = db.session.execute('select max(userid) from User_info')
    base_id = 6200000
    for ids in get_id:
      old = ids[0]
      if old is not None:
        if old >= base_id:
          userid = int(old) + 1
      else:
        userid = base_id
    newUser = User_info(username, userid, imagename, email, password, age, sex, timeinfo())
    db.session.add(newUser)
    db.session.commit()
    nu = User_info.query.filter_by(username=username).first()
    return redirect('/profile/'+str(nu.id)) 
  return render_template('form.html', form=form)
  
  
@app.route('/profiles/', methods=["GET", "POST"])
def profiles():
  users = db.session.query(User_info).all()
  if request.method == "POST":
    lst=[]
    for user in users:
      lst.append({'user_id':user.userid, 'uname':user.username})
    users = {'users': lst}
    return Response(json.dumps(users), mimetype='application/json')
  else:
    return render_template('profiles.html', users=users)
    
@app.route('/profile/<userid>', methods=['POST', 'GET'])
def user_profile(userid):
  usr = User_info.query.filter_by(id=userid).first()
  if usr is not None:
    imgURL = url_for('static', filename='img/'+usr.image)
    if request.method == 'POST':
      return jsonify(userid=usr.userid, uname=usr.username, image=imgURL, sex=usr.sex, age=usr.age, profile_added_on=usr.datejoined)
    else:
      user = {'id':usr.id, 'userid':usr.userid, 'uname':usr.username, 'image':imgURL, 'age':usr.age, 'email':usr.email, 'sex':usr.sex}
      return render_template('user.html', user=user, datestr=date_to_str(usr.datejoined))
  else:
    return render_template('404.html')
  
def date_to_str(dt):
  return dt.strftime("%a, %d %b, %Y")


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
