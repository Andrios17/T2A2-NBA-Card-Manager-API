from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp


# Establishes the Bid models
class Bid(db.Model):
    __tablename__ = 'bids'

    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[int] = mapped_column(Integer())
    date: Mapped[date]

    # Foreign Keys
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    auction_id: Mapped[int] = mapped_column(ForeignKey('auctions.id'))

    # Relationships with other tables
    user = relationship('User', back_populates='bid')
    auction = relationship('Auction', back_populates='bid')


class BidSchema(ma.Schema):

    # Allows relationships to be displayed in API endpoints
    user = fields.Nested('UserSchema', only=('username',))
    auction = fields.Nested('AuctionSchema', only=('start_date', 'end_date', 'start_price'))

    # Defines the fields to be displayed in API endpoints
    class Meta:
        fields = ('id', 'price', 'date', 'user_id', 'auction_id', 'user')
