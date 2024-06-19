from datetime import timedelta
from flask import request, Blueprint
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token
from sqlalchemy import or_
from init import db, bcrypt


users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/register', methods=['POST'])
def register():
    params = UserSchema(only=['email', 'password', 'username', 'first_name', 'last_name']).load(request.json, unknown='exclude')
    stmt = db.select(User).where(or_(User.email == params['email'], User.username == params['username']))
    user = db.session.scalar(stmt)
    if user:
        return {'message': 'User already exists'}, 400
    else:
        user = User(
            email=params['email'],
            password=bcrypt.generate_password_hash(params['password']).decode('utf8'),
            username=params['username'],
            first_name=params['first_name'],
            last_name=params['last_name'],
            is_admin=False,
        )
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created, Please login using the credentials you just created'}, 201

@users_bp.route('/login', methods=['POST'])
def login():
    params = UserSchema(only=['email', 'password']).load(request.json, unknown='exclude')
    stmt = db.select(User).where((User.email == params['email']))
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, params['password']):
        token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
        return {'message': 'Login Successful', 'token': token}, 200
    else:
        return {'message': 'Invalid Credentials'}, 401