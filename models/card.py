from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, Integer, String
from init import db


class Card(db.Model):
    __tablename__ = 'cards'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    team_name: Mapped[str] = mapped_column(String(100))
    position: Mapped[str] = mapped_column(String(3))
    set: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer())
