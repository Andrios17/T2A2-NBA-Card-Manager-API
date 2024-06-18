from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from init import db

class PersonalCollection(db.Model):
    __tablename__ = 'personal_collections'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    card_id: Mapped[int] = mapped_column(ForeignKey('cards.id'))