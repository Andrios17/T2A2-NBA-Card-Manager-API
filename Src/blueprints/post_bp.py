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

# Read all posts with their comments (R)
@posts_bp.route('/', methods=['GET'])
def get_all_posts():
    # Will query all posts within the database
    stmt = db.select(Post)
    posts = db.session.scalars(stmt).all()
    if posts:
        return PostSchema(many=True).dump(posts), 200
    else:
        return {'message': 'No posts found'}, 200

# Get a post with its comments (R)
@posts_bp.route('/<int:id>', methods=['GET'])
def get_post(id):
    # Will query the database for a post by its id, will 404 if not found
    post = db.session.query(Post).get(id)
    if post:
        return PostSchema().dump(post), 200
    else:
        return {'error': 'Post does not exist'}, 404

# Create a new post (C)
@posts_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    params = PostSchema(only=['title', 'description']).load(request.json, unknown='exclude')
    author = get_jwt_identity()
    # Will query to the users table to see if the id which is utilised to login into this route is one of a registered user
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

# Update a post (U)
@posts_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_post(id):
    params = PostSchema(only=['title', 'description']).load(request.json, unknown='exclude')
    # Will search the database to see if the id which has been entered into the route, corresponds to a post within the database
    post = db.get_or_404(Post, id)
    # Will determine whether the user accessing the route is the user of the card which is being updated
    admin_or_owner(post)
    post.title = params.get('title', post.title)
    post.description = params.get('description', post.description)
    db.session.commit()
    return PostSchema().dump(post), 200
    

# Delete a post (D)
@posts_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    # Will query the database to see if the post which is being deleted actually exists
    post = db.get_or_404(Post, id)
    # Will query to the comments table to see if there are any comments associated with the post which is being deleted
    stmt = db.select(Comment).where(Comment.post_id == id)
    comments = db.session.scalars(stmt).all()
    admin_or_owner(post)
    for comment in comments:
        db.session.delete(comment)
        db.session.commit()
    db.session.delete(post)
    db.session.commit()
    return {'message': 'Post deleted and all associated comments (if any) deleted'}, 200

# Create a comment (C)
@posts_bp.route('/comments/<int:id>', methods=['POST'])
@jwt_required()
def create_comment(id):
    identity = get_jwt_identity()
    # Will query the databse to establish whether the user accessing this route is authenticated
    stmt1 = db.select(User).where(User.id == identity)
    user = db.session.scalar(stmt1)
    # will query whether the post which this comment related to is actually present within the database
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

# Update a comment (U)
@posts_bp.route('/comments/<int:id>/<int:comment>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(id, comment):
    # Will see if the post actually exists, will 404 otherwise
    post = db.get_or_404(Post, id)
    identity = get_jwt_identity()
    admin_or_owner(post)
    # Will query the database to establish whether the user is the owner of the comment, it actually exists and whether it matches the post it relates to. 
    stmt = db.select(Comment).where(and_(Comment.id == comment, Comment.user_id == identity, Comment.post_id == id))
    comment = db.session.scalar(stmt)
    if comment:
        params = CommentSchema().load(request.json, unknown='exclude')
        comment.message = params['message']
        db.session.commit()
        return CommentSchema().dump(comment), 200
    else:
        return {'error': 'comment does not exist'}, 404

# Delete a comment (D)
@posts_bp.route('/comments/<int:id>/<int:comment>', methods=['DELETE'])
@jwt_required()
def delete_comment(id, comment):
    # Will see if the comment actually exists, will 404 otherwise
    post = db.get_or_404(Post, id)
    identity = get_jwt_identity()
    # Will see if the user owns the comment and whether comment actually exists, will ensue the comment relates to the correct post for extra data integrity
    stmt = db.select(Comment).where(and_(Comment.id == comment, Comment.user_id == identity, Comment.post_id == id))
    comment = db.session.scalar(stmt)
    if comment:
        admin_or_owner(comment)
        db.session.delete(comment)
        db.session.commit()
        return {'message': 'Comment deleted'}, 200
    else:
        return {'Error': 'Comment does not exist'}, 404