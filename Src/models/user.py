from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, Boolean
from marshmallow.validate import Length, Regexp, And
from marshmallow import fields
from typing import Optional, List
from init import db, ma

# Establishes the User models
class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships with other tables
    comment = db.relationship('Comment', back_populates='user')
    auction = db.relationship('Auction', back_populates='user')
    bid = db.relationship('Bid', back_populates='user')
    post = db.relationship('Post', back_populates='user')
    personal_collections = db.relationship('PersonalCollection', back_populates='user')

class UserSchema(ma.Schema):
    # Validation for user inputs
    email = fields.Email()
    password = fields.String(validate=Length(min=10, error='Password must be at least 10 characters'))
    username = fields.String(validate=And(
        Length(max=38, error='Username cannot be longer than 38 characters'),
        Regexp('^[a-zA-Z0-9]+$', error='Username can only contain letters and numbers')
    ))
    is_admin = fields.Boolean(default=False)

    # Defines the fields to be displayed in API endpoints
    class Meta:
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'is_admin')
