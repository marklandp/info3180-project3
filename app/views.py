#!flask/bin/python
import six
from flask import Flask, jsonify, abort, request, make_response, url_for, g
import requests
import time
from bs4 import BeautifulSoup
import urlparse
from app import app, db
from app.models import User_info
from flask_httpauth import HTTPBasicAuth
#from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
#app = Flask(__name__, static_url_path="")


# @app.errorhandler(400)
# def bad_request(error):
#     return make_response(jsonify({'error': 'Bad request'}), 400)


# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)
auth = HTTPBasicAuth()

# @auth.verify_password
# def verify_password(email_or_token, password):
#     # first try to authenticate by token
#     user = User_info.verify_auth_token(email_or_token)
#     if not user:
#         # try to authenticate with username/password
#         user = User_info.query.filter_by(email=email_or_token).first()
#         if not user or not user.verify_password(password):
#             return False
#     g.user = user
#     return True


@app.route('/api/thumbnail/process', methods=['POST'])
def process():
  images = []
  url = request.form['url']
  result = requests.get(url)
  data = result.text
  soup = BeautifulSoup(data, 'html.parser')
  og_image = (soup.find('meta', property='og:image') or
                      soup.find('meta', attrs={'name': 'og:image'}))
  if og_image and og_image['content']:
    images.append(og_image['content'])
    print og_image['content']
    
  thumbnail_spec = soup.find('link', rel='image_src')
  if thumbnail_spec and thumbnail_spec['href']:
    images.append(thumbnail_spec['href'])
    print thumbnail_spec['href']
        
  for img in soup.find_all("img", class_="a-dynamic-image"):
    if "sprite" not in img["src"]:
      images.append(img['src'])
      print img['src']
  
  if len(images) > 0:
    return jsonify({'error': 'null', 'data': {'thumbnails': images }, 'message':'success'})
  return jsonify({'error': '1', 'data':'', 'message':'Unable to extract thumbnails'})
  
@app.route('/api/user/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email'] 
    password = request.form['password']
    if email and password:
      if User_info.query.filter_by(email = email).first() is None:
        newuser = User_info(name, email, password)
        db.session.add(newuser)
        db.session.commit()
        time.sleep(2)
        added = User_info.query.filter_by(email = email).first()
        token = added.generate_auth_token(1200) 
        return jsonify({'error':'null', 'data':{'token': token.decode('ascii'), 'expires': 1200, 'user':{'_id': added.id, 'email': added.email, 'name': added.name}, 'message':'success'}})
      return jsonify({'error': '1', 'data':User_info.query.filter_by(email = email).first(), 'message':'user already exists'})
      
@app.route('/api/user/login', methods=['POST'])
def login():
    # first try to authenticate by token
    email = request.form['email']
    password = request.form['password']
    user = User_info.query.filter_by(email=email).first()
    if user and user.verify_password(password):
      g.user = user
      #time.sleep(2)
      #s = Serializer(app.config['SECRET_KEY'], expires_in = 1200)
      #token = s.dumps({'id': 2})
      token = g.user.generate_auth_token(1200) 
      return jsonify({'error':'null', 'data':{'token': token.decode('ascii'), 'expires': 1200, 'user':{'_id': g.user.id, 'email': g.user.email, 'name': g.user.name}, 'message':'success'}})
      #return jsonify({'error':'null', 'data':{'user':{'id':g.user.id, 'name':g.user.name, 'email':g.user.email}}, 'message':'success'})
    return jsonify({'error': '1', 'data':{}, 'message':'Bad user name or password'})
   


if __name__ == '__main__':
    app.run(debug=True)