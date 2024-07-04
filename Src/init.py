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

# Allowes MA schemas to be sorted in order they are created
app.json.sort_keys = False 

# Fetches the database identifer so the app can connect to the database
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

# Establishes the secret key for JWT authenication
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')

# Initializes marshmallow capabilities
ma = Marshmallow(app)
# Initializes JWT generation capabilities
jwt = JWTManager(app)
# Initializes Password hashing capabilities
bcrypt = Bcrypt(app)
# Initializes connects the models created to the database 
db = SQLAlchemy(model_class=Base)
db.init_app(app)