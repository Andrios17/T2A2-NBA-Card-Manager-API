from datetime import datetime, timedelta, date
from flask import Blueprint, request
from models.auction import Auction, AuctionSchema
from models.bid import Bid, BidSchema
from models.pc import PersonalCollection
from models.card import Card, CardSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from sqlalchemy import and_
from sqlalchemy.exc import DataError

auction_bp = Blueprint('auction', __name__, url_prefix='/auction')

# Get all auctions in the database (R)
@auction_bp.route('/', methods=['GET'])
def get_all_auctions():
    # Will query all auctions within the database
    stmt = db.select(Auction)
    auctions = db.session.scalars(stmt).all()
    return AuctionSchema(many=True).dump(auctions),200

# Get a specific auction (R)
@auction_bp.route('/<int:id>', methods=['GET'])
def get_auction(id):
    # Will query an auction by its id within the database
    stmt = db.select(Auction).where(Auction.id == id)
    auction = db.session.scalar(stmt)
    if auction:
        return AuctionSchema().dump(auction), 200
    else:
        return {'message': 'Auction does not exist'}, 404

# Get a card by its id and auctions (R)
@auction_bp.route('/card/<int:id>', methods=['GET'])
def get_all_auctions_on_one_card(id):
    # Will ensure that the card that is being searched for actually exists in the database
    card = db.get_or_404(Card, id)
    # Searches for all auctions that relate to the card in the database
    stmt = db.select(Auction).where(Auction.card_id == id) 
    auctions = db.session.scalars(stmt).all()
    if auctions:
        return AuctionSchema(many=True).dump(auctions), 200
    else:
        return {'message': 'No auctions found for this card'}, 200


# Create a new auction (C)
@auction_bp.route('/', methods=['POST'])
@jwt_required()
def create_auction():
    identity = get_jwt_identity()
    params = AuctionSchema(only=['end_date', 'start_price', 'card_id']).load(request.json, unknown='exclude')
    # Will query the users personal_collection entities as for a user to place a card on auction, the card itself must already exist in that users personal_collection, 
    # Will utilise the entered card_id as the search parameters in the query
    stmt = db.select(PersonalCollection).where(and_(PersonalCollection.user_id == identity, PersonalCollection.card_id == params['card_id']))
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
        return {'message': 'Card does not exist in the users personal collection'}, 401


# Update an auction (U)
@auction_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_auction(id):
    # Will query the database to see if the auction exists utilising the auction_id entered, will 404 if not found
    auction = db.get_or_404(Auction, id)
    identity = get_jwt_identity()
    # Will query the database to see if the auction which is being updated has been created by the user who is accessing this route
    stmt = db.select(Auction).where(and_(Auction.id == id, Auction.user_id == identity))
    auction = db.session.scalar(stmt)
    if auction:
        params = AuctionSchema(only=['end_date']).load(request.json, unknown='exclude')
        auction.end_date = params.get('end_date', auction.end_date)
        db.session.commit()
        return AuctionSchema().dump(auction), 200
    else:
        return {'message': 'Unauthorized or auction does not exist'}, 401

# Delete an auction (D)
@auction_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_auction(id):
    # Will query the database to see if the auction exists utilising the auction_id entered, will 404 if not found
    auction = db.get_or_404(Auction, id)
    identity = get_jwt_identity()
    # Will query the database to see if the auction which is being deleted has been created by the user who is accessing this route
    stmt = db.select(Auction).where(and_(Auction.id == id, auction.user_id == identity))
    auction = db.session.scalar(stmt)
    if auction:
        # Will query the database to see if the auction which is being deleted, has any bids associated with it
        stmt = db.select(Bid).where(Bid.auction_id == auction.id)
        bids = db.session.scalars(stmt).all()
        # If there are any bids associated with the auction, the following block of code will be executed to delete these bids
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


# Create a new bid (C)
@auction_bp.route('/bid/<int:id>', methods=['POST'])
@jwt_required()
def create_bid(id):
    # Will query the database to see if the auction which is being bid on exists, will 404 if not found
    auction = db.get_or_404(Auction, id)
    identity = get_jwt_identity()
    # Will check if the user trying to place a bid is the owner of the auction, if not, they will be able to place a bid.
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
        return {'message': 'Unauthorized, you are the owner of the auction and cannot bid'}, 401


# Update a bid (U)
@auction_bp.route('/bid/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_bid(id):
    # Will query the database to see if the bid exists utilising the bid_id entered, will 404 if not found
    bid = db.get_or_404(Bid, id)
    identity = get_jwt_identity()
    # If the identity of the user matches the identity of the user who submitted the bid, they will be able to update the bid
    if identity == bid.user_id:
        params = BidSchema(only=['price']).load(request.json, unknown='exclude')
        bid.price = params.get('price', bid.price)
        db.session.commit()
        return BidSchema().dump(bid), 200
    else:
        return {'message': 'Unauthorized, you are not the owner of this bid'}, 401


# Delete a bid (D)
@auction_bp.route('/bid/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_bid(id):
    # Will query the database to see if the bid exists utilising the bid_id entered, will 404 if not found
    bid = db.get_or_404(Bid, id)
    identity = get_jwt_identity()
    if identity == bid.user_id:
        db.session.delete(bid)
        db.session.commit()
        return {'message': 'Bid deleted'}, 200
    else:
        return {'message': 'Unauthorized'}, 401


# Error handling for invalid data types in JSON payloads
@auction_bp.errorhandler(DataError)
def ints_only(err):
    return {'error': 'please ensure you using ints when entering price and starting price'}, 400