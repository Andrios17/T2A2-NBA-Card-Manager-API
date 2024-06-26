from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from models.user import User, UserSchema
from sqlalchemy import  String, Text, ForeignKey 
from typing import Optional
from init import db, ma
from marshmallow import fields

class Comment(db.Model):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(Text())
    date_posted: Mapped[date]

    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user = db.relationship('User', back_populates='comment')
    post = db.relationship('Post', back_populates='comment')

class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=('username',))

    class Meta:
        fields = ('id', 'message', 'date_posted', 'user')