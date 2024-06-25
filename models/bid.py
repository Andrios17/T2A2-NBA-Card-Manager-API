from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from init import db, ma
from marshmallow import fields

class Bid(db.Model):
    __tablename__ = 'bids'

    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[int] = mapped_column(Integer())
    date: Mapped[date]
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    auction_id: Mapped[int] = mapped_column(ForeignKey('auctions.id'))

    user = relationship('User', back_populates='bid')
    auction = relationship('Auction', back_populates='bid')


class BidSchema(ma.Schema):
    user = fields.Nested('UserSchema')
    auction = fields.Nested('AuctionSchema', only=('start_date', 'end_date', 'start_price', ))
    class Meta:
        fields = ('id', 'price', 'date', 'user_id', 'auction_id', 'auction')
