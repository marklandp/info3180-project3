from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost/proj3?client_encoding=utf8"
app.config['SECRET_KEY'] = "oh wow i did not remember to add this, hehe"
db = SQLAlchemy(app)

from app import views, models


