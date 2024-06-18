from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

class Base(DeclarativeBase):
    pass

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')

ma = Marshmallow(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(model_class=Base)
db.init_app(app)