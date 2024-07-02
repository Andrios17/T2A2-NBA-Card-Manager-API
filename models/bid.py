from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp

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
    price = fields.Int(validate=(Regexp('^[0-9]+$', error='Invalid, Price must be a whole number')))

    user = fields.Nested('UserSchema', only=('username',))
    auction = fields.Nested('AuctionSchema', only=('start_date', 'end_date', 'start_price'))

    class Meta:
        fields = ('id', 'price', 'date', 'user_id', 'auction_id', 'user')
