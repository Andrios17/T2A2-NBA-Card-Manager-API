from datetime import datetime, timedelta, date
from flask import Blueprint, request
from models.auction import Auction, AuctionSchema
from models.bid import Bid, BidSchema
from models.pc import PersonalCollection
from models.card import Card, CardSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from sqlalchemy import and_

auction_bp = Blueprint('auction', __name__, url_prefix='/auction')

@auction_bp.route('/', methods=['GET'])
def get_all_auctions():
    stmt = db.select(Auction)
    auctions = db.session.scalars(stmt).all()
    return AuctionSchema(many=True).dump(auctions),200

@auction_bp.route('/<int:id>', methods=['GET'])
def get_auction(id):
    stmt = db.select(Auction).where(Auction.id == id)
    auction = db.session.scalar(stmt)
    if auction:
        return AuctionSchema().dump(auction), 200
    else:
        return {'message': 'Auction does not exist'}, 404

@auction_bp.route('/card/<int:id>', methods=['GET'])
def get_all_auctions_on_one_card(id):
    card = db.get_or_404(Card, id)
    stmt = db.select(Auction).where(Auction.card_id == id) 
    auctions = db.session.scalars(stmt).all()
    if auctions:
        return AuctionSchema(many=True).dump(auctions), 200
    else:
        return {'message': 'No auctions found for this card'}, 200

@auction_bp.route('/', methods=['POST'])
@jwt_required()
def create_auction():
    identity = get_jwt_identity()
    params = AuctionSchema(only=['end_date', 'start_price', 'card_id']).load(request.json, unknown='exclude')
    stmt = db.select(PersonalCollection).where(and_(PersonalCollection.id == identity, PersonalCollection.card_id == params['card_id']))
    pc = db.session.scalar(stmt)
    if pc:
        auction = Auction(
            start_date= date.today(),
            end_date=params['end_date'],
            start_price=params['start_price'],
            card_id=params['card_id'],
            user_id=get_jwt_identity()
        )
        db.session.add(auction)
        db.session.commit()
        return AuctionSchema().dump(auction), 201
    else:
        return {'message': 'Unauthorized or card does not exist'}, 401
    

@auction_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_auction(id):
    auction = db.get_or_404(Auction, id)
    identity = get_jwt_identity()
    stmt = db.select(Auction).where(and_(Auction.id == id, auction.user_id == identity))
    auction = db.session.scalar(stmt)
    if auction:
        params = AuctionSchema(only=['end_date']).load(request.json, unknown='exclude')
        auction.end_date = params.get('end_date', auction.end_date)
        db.session.commit()
        return AuctionSchema().dump(auction), 200
    else:
        return {'message': 'Unauthorized or auction does not exist'}, 401

@auction_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_auction(id):
    auction = db.get_or_404(Auction, id)
    identity = get_jwt_identity()
    stmt = db.select(Auction).where(and_(Auction.id == id, auction.user_id == identity))
    auction = db.session.scalar(stmt)
    if auction:
        stmt = db.select(Bid).where(Bid.auction_id == auction.id)
        bids = db.session.scalars(stmt).all()
        if bids:
            for bid in bids:
                db.session.delete(bid)
                db.session.commit()
            db.session.delete(auction)
            db.session.commit()
            return {'message': 'Auction and all bids associated deleted'}, 200
        else:
            db.session.delete(auction)
            db.session.commit()
            return {'message': 'Auction deleted'}, 200
    else:
        return {'message': 'Unauthorized or auction does not exist'}, 401

@auction_bp.route('/bid/<int:id>', methods=['POST'])
@jwt_required()
def create_bid(id):
    auction = db.get_or_404(Auction, id)
    identity = get_jwt_identity()
    if identity != auction.user_id:
        params = BidSchema(only=['price']).load(request.json, unknown='exclude')
        bid = Bid(
            date = date.today(),
            price = params['price'],
            user_id = identity,
            auction_id = auction.id
        )
        db.session.add(bid)
        db.session.commit()
        return BidSchema().dump(bid), 201
    else:
        return {'message': 'Unauthorized'}, 401

@auction_bp.route('/bid/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_bid(id):
    bid = db.get_or_404(Bid, id)
    identity = get_jwt_identity()
    if identity == bid.user_id:
        params = BidSchema(only=['price']).load(request.json, unknown='exclude')
        bid.price = params.get('price', bid.price)
        db.session.commit()
        return BidSchema().dump(bid), 200
    else:
        return {'message': 'Unauthorized'}, 401

@auction_bp.route('/bid/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_bid(id):
    bid = db.get_or_404(Bid, id)
    identity = get_jwt_identity()
    if identity == bid.user_id:
        db.session.delete(bid)
        db.session.commit()
        return {'message': 'Bid deleted'}, 200
    else:
        return {'message': 'Unauthorized'}, 401