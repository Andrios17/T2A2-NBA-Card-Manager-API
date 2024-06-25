from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String
from init import db, ma
from typing import Optional, List


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
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'team_name', 'position', 'set', 'year')