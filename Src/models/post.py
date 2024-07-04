from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  String, Text, ForeignKey
from marshmallow.validate import Length, Regexp, And
from typing import Optional
from init import db, ma
from marshmallow import fields


# Establishes the Post models
class Post(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[Optional[str]] = mapped_column(String(250))
    description: Mapped[Optional[str]] = mapped_column(Text())
    date_posted: Mapped[date]

    # Foreign keys
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    # Relationships with other tables
    comment = db.relationship('Comment', back_populates='post')
    user = db.relationship('User', back_populates='post')

class PostSchema(ma.Schema):
    # Allowes relationships to be displayed in API endpoints
    comment=fields.List(fields.Nested("CommentSchema"))
    user= fields.Nested('UserSchema', only= ('username',))

    # Validation for user inputs
    title=fields.String(required=True, validate=And(
        Regexp('^[0-9a-zA-Z ]+$', error='Title must only contain alphanumeric characters'),
        Length(min=10, max=250, error='Title cannot be shorter than 10 characters or longer than 250 characters')
    ))
    description=fields.String(required=False, validate=Length(max=63000, error='Description must be less than 63,000 characters'))

    # Defines the fields to be displayed in API endpoints
    class Meta:
        ordered = True
        fields = ('id', 'user', 'title', 'description', 'date_posted','comment')
