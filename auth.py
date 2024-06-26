from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.user import User
from functools import wraps

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