from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from init import db, ma
from marshmallow import fields, validate


# Establishes the PersonalCollection models
class PersonalCollection(db.Model):
    __tablename__ = 'personal_collections'

    id: Mapped[int] = mapped_column(primary_key=True)

    # Foreign keys
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    card_id: Mapped[int] = mapped_column(ForeignKey('cards.id'))

    # Relationships with other tables
    card = relationship('Card', back_populates="personal_collections")
    user = relationship('User', back_populates='personal_collections')

class PersonalCollectionSchema(ma.Schema):    
    # Allows relationships to be displayed in API endpoints
    card = fields.Nested('CardSchema')

    # Defines the fields to be displayed in API endpoints
    class Meta:
        fields = ('id', 'user_id', 'card_id', 'card')