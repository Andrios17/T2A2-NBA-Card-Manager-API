from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.user import User
from functools import wraps
from sqlalchemy import or_
from flask import abort, jsonify, make_response

def admin_only(fn):
    @wraps(fn)
    @jwt_required()
    def inner():
        user_id = get_jwt_identity()
        stmt = db.select(User).where(User.id == user_id, User.is_admin)
        user = db.session.scalar(stmt)
        if(user):
            return fn()
        else:
            return {'error': 'Not Authorized, Must be an admin'}, 403
    return inner

def admin_only_search(fn):
    @wraps(fn)
    @jwt_required()
    def inner(id):
        user_id = get_jwt_identity()
        stmt = db.select(User).where(User.id == user_id, User.is_admin)
        user = db.session.scalar(stmt)
        if(user):
            return fn(id)
        else:
            return {'error': 'Not Authorized, Must be an admin'}, 403
    return inner

def admin_or_owner(reference):
    id = get_jwt_identity()
    stmt = db.select(User).where(User.id == id, User.is_admin)
    admin = db.session.scalar(stmt)
    if id == reference.user_id:
        return
    elif not admin:
        abort(make_response(jsonify(error= 'Not Authorized, Must be an admin or owner to alter this'), 403))