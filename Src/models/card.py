from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String
from init import db, ma
from typing import Optional, List
from marshmallow import fields
from marshmallow.validate import Length, Regexp, And


class Card(db.Model):
    __tablename__ = 'cards'

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    team_name: Mapped[str] = mapped_column(String(100))
    position: Mapped[str] = mapped_column(String(3))
    set: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer())

    personal_collections = relationship('PersonalCollection', back_populates='card')
    auction = relationship('Auction', back_populates='card')


class CardSchema(ma.Schema):
    first_name = fields.String(required=True, validate=Regexp(r'^[a-zA-Z0-9.\- ]+$', error='First name can only contain letters, numbers, full stops, hyphens and spaces'))
    last_name = fields.String(required=True, validate=Regexp(r'^[a-zA-Z0-9.\- ]+$', error='Last name can only contain letters, numbers, full stops, hyphens and spaces'))
    team_name = fields.String(required=True, validate=Regexp(r'^[a-zA-Z0-9.\- ]+$', error='Team name can only contain letters, numbers, full stops, hyphens and spaces'))
    position = fields.String(required=True, validate=Regexp('^[A-Z]+$', error='Position can only contain capital letters'))
    set = fields.String(required=True, validate=Length(max=300, error='Set name cannot be longer than 300 characters'))
    year = fields.Int(required=True)

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'team_name', 'position', 'set', 'year')