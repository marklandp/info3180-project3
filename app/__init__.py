from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ztlngjrnvziegs:Ev9h62QPQYd0zyiTZipZsGbmDD@ec2-54-204-35-248.compute-1.amazonaws.com:5432/dfqlm57b31f0ab'
db = SQLAlchemy(app)

from app import views, models


