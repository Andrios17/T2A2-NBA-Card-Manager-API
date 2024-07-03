from datetime import date
from flask import request, Blueprint
from models.post import Post, PostSchema
from models.user import User, UserSchema
from models.comment import Comment, CommentSchema
from init import db, ma
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_
from auth import admin_or_owner

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

# Read all posts with their comments
@posts_bp.route('/', methods=['GET'])
def get_all_posts():
    stmt = db.select(Post)
    posts = db.session.scalars(stmt).all()
    if posts:
        return PostSchema(many=True).dump(posts), 200
    else:
        return {'message': 'No posts found'}, 200

# Get a post with its comments
@posts_bp.route('/<int:id>', methods=['GET'])
def get_post(id):
    post = db.session.query(Post).get(id)
    if post:
        return PostSchema().dump(post), 200
    else:
        return {'error': 'Post does not exist'}, 404

# Create a new post
@posts_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    params = PostSchema(only=['title', 'description']).load(request.json, unknown='exclude')
    author = get_jwt_identity()
    stmt = db.select(User).where(User.id == author)
    author = db.session.scalar(stmt)
    post = Post(
        title=params.get('title'),
        description=params.get('description',''),
        date_posted=date.today(),
        user_id=get_jwt_identity(),
    )
    db.session.add(post)
    db.session.commit()
    return PostSchema().dump(post), 201

# Update a post
@posts_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_post(id):
    params = PostSchema(only=['title', 'description']).load(request.json, unknown='exclude')
    post = db.get_or_404(Post, id)
    admin_or_owner(post)
    post.title = params.get('title', post.title)
    post.description = params.get('description', post.description)
    db.session.commit()
    return PostSchema().dump(post), 200
    

# Delete a post
@posts_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    post = db.get_or_404(Post, id)
    stmt = db.select(Comment).where(Comment.post_id == id)
    comments = db.session.scalars(stmt).all()
    admin_or_owner(post)
    for comment in comments:
        db.session.delete(comment)
        db.session.commit()
    db.session.delete(post)
    db.session.commit()
    return {'message': 'Post deleted and all associated comments (if any) deleted'}, 200

# Create a comment
@posts_bp.route('/comments/<int:id>', methods=['POST'])
@jwt_required()
def create_comment(id):
    identity = get_jwt_identity()
    stmt1 = db.select(User).where(User.id == identity)
    user = db.session.scalar(stmt1)
    stmt2 = db.select(Post).where(Post.id == id)
    post = db.session.scalar(stmt2)
    if user and post:
        params = CommentSchema().load(request.json, unknown='exclude')
        comment = Comment(
            message=params['message'],
            date_posted=date.today(),
            post_id=id,
            user_id=identity
        )
        db.session.add(comment)
        db.session.commit()
        return CommentSchema().dump(comment), 201
    else:
        return {'message': 'Unauthorized or post does not exist'}, 401

# Update a comment
@posts_bp.route('/comments/<int:id>/<int:comment>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(id, comment):
    post = db.get_or_404(Post, id)
    identity = get_jwt_identity()
    admin_or_owner(post)
    stmt = db.select(Comment).where(and_(Comment.id == comment, Comment.user_id == identity, Comment.post_id == id))
    comment = db.session.scalar(stmt)
    if comment:
        params = CommentSchema().load(request.json, unknown='exclude')
        comment.message = params['message']
        db.session.commit()
        return CommentSchema().dump(comment), 200
    else:
        return {'error': 'comment does not exist'}, 404

# Delete a comment
@posts_bp.route('/comments/<int:id>/<int:comment>', methods=['DELETE'])
@jwt_required()
def delete_comment(id, comment):
    post = db.get_or_404(Post, id)
    identity = get_jwt_identity()
    stmt = db.select(Comment).where(and_(Comment.id == comment, Comment.user_id == identity, Comment.post_id == id))
    comment = db.session.scalar(stmt)
    if comment:
        admin_or_owner(comment)
        db.session.delete(comment)
        db.session.commit()
        return {'message': 'Comment deleted'}, 200
    else:
        return {'Error': 'Comment does not exist'}, 404