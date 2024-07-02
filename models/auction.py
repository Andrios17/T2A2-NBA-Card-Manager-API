from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from marshmallow.validate import Regexp
from init import db, ma
from marshmallow import fields

class Auction(db.Model):
    __tablename__ = 'auctions'

    id: Mapped[int] = mapped_column(primary_key=True)
    start_date: Mapped[date]
    end_date: Mapped[date]
    start_price: Mapped[int] = mapped_column(Integer())

    card_id: Mapped[int] = mapped_column(ForeignKey('cards.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user = relationship('User', back_populates='auction')
    card = relationship('Card', back_populates='auction')
    bid = relationship('Bid', back_populates='auction')


class AuctionSchema(ma.Schema):
    end_date = fields.Date(required=True, format="%Y-%m-%d")
    start_price = fields.Int(validate=(Regexp('^[0-9]+$', error='Invalid, Starting_Price must be a whole number')))

    user = fields.Nested('UserSchema', only=('username', 'id'))
    card = fields.Nested('CardSchema', only=('first_name', 'last_name', 'set', 'year', 'team_name'))
    bid = fields.List(fields.Nested('BidSchema', exclude=('auction_id',)))

    class Meta:
        fields = ('id', 'card', 'start_date', 'end_date', 'start_price', 'card_id', 'user', 'bid')