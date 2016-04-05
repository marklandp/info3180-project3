#!flask/bin/python
import six
from flask import Flask, jsonify, abort, request, Response, url_for, g, session
import json
import requests
import time
from bs4 import BeautifulSoup
import urlparse
import urllib2
from app import app, db
from app.models import User_info, Wishes
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@app.route('/')
def home():
  return jsonify({'message':'Welcome to the wishlist system. This system has no gui you can use this site by sending curl requests to routes defined in this doc ==> https://docs.google.com/document/d/1edz3AW5Eq3ZZ2qgoZpo_9j0zNNb3SkPs5k4EO7RJ_kU/edit#heading=h.6ofmligdv9pv. Part 3 of the document. 620011825'})

@app.route('/api/thumbnail/process', methods=['POST'])
def process():
  images = []
  url = request.form['url']
  hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
  req = urllib2.Request(url, headers=hdr)
  data = urllib2.urlopen(req)
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
    if "sprite" not in img["src"] and "data:image/jpeg" not in img["src"]:
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
      return jsonify({'error': '1', 'data':'', 'message':'user already exists'})
      
@app.route('/api/user/login', methods=['POST'])
def login():
    email_or_token = request.form['email']
    password = request.form['password']
    user = User_info.query.filter_by(email=email_or_token).first()
    if user and user.verify_password(password):
      g.user = user
      token = g.user.generate_auth_token(1200) 
      return jsonify({'error':'null', 'data':{'token': token.decode('ascii'), 'expires': 1200, 'user':{'_id': g.user.id, 'email': g.user.email, 'name': g.user.name}, 'message':'success'}})
    return jsonify({'error': '1', 'data':{}, 'message':'Bad user name or password'})
    
@app.route('/api/user/<id>/wishlist', methods=['GET', 'POST'])
def wish(id):
  if request.method == "POST":
    title = request.form['title']
    desc = request.form['description']
    thumb = request.form['thumbnail']
    url = request.form['url']
    user = User_info.query.filter_by(id=id).first()
    if user:
      wishes = Wishes.query.filter_by(user=id).all()
      for wish in wishes:
        if url in wish.url:
          return jsonify({'error':'2', 'data':'', 'message':'url item already exists'})
        wish = Wishes(title,desc,thumb,id,url)
        db.session.add(wish)
        db.session.commit()
        time.sleep(2)
        allwishes = Wishes.query.filter_by(user=id).all()
        lst=[]
        for wish in allwishes:
          lst.append({'title':wish.title, 'description':wish.description, 'url':wish.url, 'thumbnail':wish.thumbnail})
        data = ({'error':'null', 'data':{'wishes': lst}, 'message':'success'})
        return jsonify(**data)
    return jsonify({'error':'1', 'data':'', 'message':'no such wishlist exists'})
	if g.user.id == id
		user = User_info.query.filter_by(id=id).first()
		if user:
			wishes = Wishes.query.filter_by(user=id).all()
			lst=[]
			for wish in wishes:
				lst.append({'title':wish.title, 'description':wish.description, 'url':wish.url, 'thumbnail':wish.thumbnail})
			data = ({'error':'null', 'data':{'wishes': lst}, 'message':'success'})
			return jsonify(**data)
		return jsonify({'error':'1', 'data':'', 'message':'no such wishlist exists'})  
	return jsonify({'error':'3', 'data':'', 'message':'unauthorized access'})

if __name__ == '__main__':
    app.run(debug=True) 