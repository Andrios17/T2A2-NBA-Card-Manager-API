from datetime import date
from flask import request, Blueprint
from models.post import Post, PostSchema
from models.user import User, UserSchema
from init import db, ma
from flask_jwt_extended import jwt_required, get_jwt_identity

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('/', methods=['GET'])
def get_all_posts():
    stmt = db.select(Post)
    posts = db.session.scalars(stmt).all()
    return PostSchema(many=True).dump(posts), 200

@posts_bp.route('/<int:id>', methods=['GET'])
def get_post(id):
    post = db.session.query(Post).get(id)
    return PostSchema().dump(post), 200

@posts_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    params = PostSchema(only=['title', 'description']).load(request.json, unknown='exclude')
    author = get_jwt_identity()
    stmt = db.select(User).where(User.id == author)
    author = db.session.scalar(stmt)
    post = Post(
        title=params['title'],
        description=params['description'],
        date_posted=date.today(),
        user_id=get_jwt_identity(),
        user_username=author.username
    )
    db.session.add(post)
    db.session.commit()
    return PostSchema().dump(post), 201

@posts_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_post(id):
    params = PostSchema().load(request.json, unknown='exclude')
    post = db.session.query(Post).get(id)
    if post.user_id == get_jwt_identity():
        post.title = params['title']
        post.description = params['description']
        db.session.commit()
        return PostSchema().dump(post), 200
    else:
        return {'message': 'Unauthorized'}, 401
    

@posts_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    post = db.session.query(Post).get(id)
    if post.user_id == get_jwt_identity():
        db.session.delete(post)
        db.session.commit()
        return {'message': 'Post deleted'}, 200
    else:
        return {'message': 'Unauthorized'}, 401