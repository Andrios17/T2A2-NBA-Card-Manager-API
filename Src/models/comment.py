from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  String, Text, ForeignKey 
from typing import Optional
from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length


# Establishes the Comment models
class Comment(db.Model):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(Text())
    date_posted: Mapped[date]

    # Foreign keys
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    # Relationships with other tables
    user = db.relationship('User', back_populates='comment')
    post = db.relationship('Post', back_populates='comment')

class CommentSchema(ma.Schema):
    # Allows relationships to be displayed in API endpoints
    user = fields.Nested('UserSchema', only=('username',))

    # Validation for user inputs
    message=fields.String(required=True, validate=Length(max=32000, error='Message must be less than 32,000 characters'))

    class Meta:
    # Defines the fields to be displayed in API endpoints
        fields = ('id', 'message', 'date_posted', 'user')