from datetime import timedelta, date
from flask import request, Blueprint
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token
from sqlalchemy import or_
from init import db, bcrypt
from auth import admin_only


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

@users_bp.route('/', methods=['GET'])
@admin_only
def get_all_users():
    users = db.session.query(User).all()
    return UserSchema(many=True).dump(users), 200

@users_bp.route('/<int:id>', methods=['GET'])
@admin_only
def get_user(id):
    user = db.get_or_404(User, id)
    return UserSchema().dump(user), 200

@users_bp.route('/edit/<int:id>', methods=['PATCH'])
@admin_only
def edit_user(id):
    user = db.get_or_404(User, id)
    params = UserSchema(only=['email', 'password', 'username', 'first_name', 'last_name', 'is_admin']).load(request.json, unknown='exclude')
    user.email = params.get('email', user.email)
    user.password = params.get('password', user.password)
    user.username = params.get('username', user.username)
    user.first_name = params.get('first_name', user.first_name)
    user.last_name = params.get('last_name', user.last_name)
    user.is_admin = params.get('is_admin', user.is_admin)
    db.session.commit()
    return UserSchema().dump(user), 200

@users_bp.route('/delete/<int:id>', methods=['DELETE'])
@admin_only
def delete_user(id):
    user = db.get_or_404(User, id)
    db.session.delete(user)
    db.session.commit()
    return {'message': 'User deleted'}, 200

@users_bp.route('/create', methods=['POST'])
@admin_only
def create_user():
    params = UserSchema(only=['email', 'password', 'username', 'first_name', 'last_name', 'is_admin']).load(request.json, unknown='exclude')
    stmt = db.select(User).where(or_(User.email == params['email'], User.username == params['username']))
    user = db.session.scalar(stmt)
    if user:
        return {'message': 'User already exists'}, 400
    else:
        user_created = User(
            email=params['email'],
            password=bcrypt.generate_password_hash(params['password']).decode('utf8'),
            username=params['username'],
            first_name=params['first_name'],
            last_name=params['last_name'],
            is_admin=params['is_admin'],
        )

        db.session.add(user_created)
        db.session.commit()
        return UserSchema().dump(user_created), 201