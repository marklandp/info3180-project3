"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

from app import app
from flask import Flask, Response, render_template, request, redirect, url_for, flash, jsonify, session, abort, g
from flask.ext.login import  LoginManager, login_user , logout_user , current_user , login_required
from app import db
from flask.ext.sqlalchemy import SQLAlchemy
from app.models import User_info, Wishes
from datetime import *
from .forms import RegistrationForm, SigninForm, WishForm
import json
from werkzeug.utils import secure_filename
from sqlalchemy.sql.expression import func
import os
import time
from bs4 import BeautifulSoup
import urlparse
import requests
import urllib2


###
# Routing for your application.
###

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

@login_manager.user_loader
def load_user(id):
    return User_info.query.get(int(id))

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
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']
    age = int(request.form['age'])
    sex = request.form['sex']
    photo = request.files['image']
    imagename = fname + '_' + secure_filename(photo.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], imagename)
    photo.save(file_path)
    newUser = User_info(fname, lname, imagename, email, password, age, sex, timeinfo())
    db.session.add(newUser)
    db.session.commit()
    flash('You have successfully registered. Login below.')
    return redirect(url_for('signin'))
  return render_template('form.html', form=form)
  
  
@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
  if g.user.is_authenticated:
    return redirect(url_for('profile'))
   
  if request.method == 'POST':
    if form.validate() == False:
      msg = "Invalid Login!"
      return render_template('signin.html', form=form, messages=msg)
    else:
      email = form.email.data.lower()
      user = User_info.query.filter_by(email=email).first()
      if user is None and form.validate() == False:
        return redirect(url_for('signin'))
      session['email'] = form.email.data
      login_user(user)
      return redirect(request.args.get('next') or url_for('profile'))
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)
    
    
@app.route('/signout')
def signout():
    logout_user()
    session['email'] = None
    return redirect(url_for('home')) 
  
  
@app.route('/profiles/', methods=["GET", "POST"])
@login_required
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
    

@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
  form = WishForm()
  wishes = Wishes.query.filter_by(user=g.user.email).all()
  image = url_for('static', filename='img/'+g.user.image)
  user = {'id':g.user.id, 'image':image, 'age':g.user.age, 'fname':g.user.fname, 'lname':g.user.lname, 'email':g.user.email, 'sex':g.user.sex}
  if wishes:
    return render_template('user.html', user=user, wishes=wishes, datestr=date_to_str(g.user.datejoined), form=form)
  return render_template('user.html', user=user, datestr=date_to_str(g.user.datejoined), form=form)
  
@app.route('/add', methods=['POST'])
@login_required
def addWish():
  form = WishForm()
  if form.validate_on_submit():
    url = request.form['url']
    result = requests.get(url)
    data = result.text
    images = []
    soup = BeautifulSoup(data, 'html.parser')
    title = (soup.find('meta', property='og:title') or 
                    soup.find('meta', attrs={'name': 'title'}))
    if title and title['content']:
      #print title['content']
      content = title['content']
    else:
      content = "Really want this"
      
    desc = (soup.find('meta', property='og:description') or 
                    soup.find('meta', attrs={'name': 'description'}))
    if desc and desc['content']:
      description = desc['content']
    else:
      description = "I want this item"
      
    og_image = (soup.find('meta', property='og:image') or 
                        soup.find('meta', attrs={'name': 'og:image'}))
    if og_image and og_image['content']:
      images.append(og_image['content'])

    for img in soup.find_all("img", class_="a-dynamic-image"):
      #print img['src']
      images.append(img['src'])

    thumbnail_spec = soup.find('link', rel='image_src')
    if thumbnail_spec and thumbnail_spec['href']:
      images.append(thumbnail_spec['href'])
      #print thumbnail_spec['href']
    if len(images) >= 1:
      return render_template('process.html', description=description, title=content, images=images, origin=url)
    else:
      desc="Unable to scrape any images from given url"
      title="Error"
      return render_template('process.html', description=desc, title=title, images=images)
  image = url_for('static', filename='img/'+g.user.image)
  user = {'id':g.user.id, 'image':image, 'age':g.user.age, 'fname':g.user.fname, 'lname':g.user.lname, 'email':g.user.email, 'sex':g.user.sex}
  return render_template('user.html', user=user, datestr=date_to_str(g.user.datejoined), form=form)
  
@app.route('/commit', methods=['POST'])
@login_required
def commit():
  if request.method == "POST":
    title = request.form['title']
    desc = request.form['description']
    thumb = request.form['thumbnail']
    origin = request.form['origin']
    user = g.user.email
    wish = Wishes(title,desc,thumb,user,origin)
    db.session.add(wish)
    db.session.commit()
    return redirect(url_for('profile'))
  return render_template('404.html')
  
    
@app.before_request
def before_request():
    g.user = current_user
    
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
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
