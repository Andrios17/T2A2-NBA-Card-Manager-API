from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from models.user import User, UserSchema
from sqlalchemy import  String, Text, ForeignKey
from typing import Optional
from init import db, ma
from marshmallow import fields

class Post(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[Optional[str]] = mapped_column(String(250))
    description: Mapped[str] = mapped_column(Text())
    date_posted: Mapped[date]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user_username: Mapped[str] = mapped_column(ForeignKey('users.username'))

    comment = db.relationship('Comment', back_populates='post')

class PostSchema(ma.Schema):
    comment=fields.List(fields.Nested("CommentSchema"))
    class Meta:
        ordered = True
        fields = ('id', 'title', 'description', 'date_posted','user_id', 'user_username', 'comment')
