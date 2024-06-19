from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, Integer, String
from init import db, ma


class Card(db.Model):
    __tablename__ = 'cards'

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    team_name: Mapped[str] = mapped_column(String(100))
    position: Mapped[str] = mapped_column(String(3))
    set: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer())


class CardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'team_name', 'position', 'set', 'year')