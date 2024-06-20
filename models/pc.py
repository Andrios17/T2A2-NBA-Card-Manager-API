from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from init import db, ma
from marshmallow import fields

class PersonalCollection(db.Model):
    __tablename__ = 'personal_collections'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    card_id: Mapped[int] = mapped_column(ForeignKey('cards.id'))

    card = relationship('Card', back_populates="personal_collections")

class PersonalCollectionSchema(ma.Schema):
    card = fields.Nested('CardSchema')
    class Meta:
        fields = ('id', 'user_id', 'card_id', 'card')