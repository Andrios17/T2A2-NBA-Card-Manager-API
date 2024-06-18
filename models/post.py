from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import  String, Text, ForeignKey 
from typing import Optional
from init import db

class Post(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[Optional[str]] = mapped_column(String(250))
    description: Mapped[str] = mapped_column(Text())
    date_posted: Mapped[date]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
