from flask import Blueprint,request
from init import db, ma
from models.card import Card, CardSchema
from auth import admin_only, admin_only_search

card_bp = Blueprint('card', __name__, url_prefix='/cards')


# Get all cards in the database (R)
@card_bp.route('/', methods=['GET'])
def get_all_cards():
    # Queries the database for all cards
    cards = db.session.query(Card).all()
    return CardSchema(many=True).dump(cards), 200


# Get a card by its id (R)
@card_bp.route('/<int:id>', methods=['GET'])
def get_card(id):
    # Queries the database for a card by its id
    card = db.session.query(Card).get(id)
    if card:
        return CardSchema().dump(card), 200
    else:
        return {'error': 'Card does not exist'}, 404


# Create a new card (C)
@card_bp.route('/', methods=['POST'])
@admin_only
def create_card():
    params = CardSchema().load(request.json, unknown='exclude')
    card = Card(
        first_name=params['first_name'],
        last_name=params['last_name'],
        team_name=params['team_name'],
        position=params['position'],
        set=params['set'],
        year=params['year']
    )
    db.session.add(card)
    db.session.commit()
    return CardSchema().dump(card), 201

# Update a card in the database (U)
@card_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@admin_only_search
def update_card(id):
    # Will ensure that the card which is being updated actually exists within the database, will 404 if not found
    card = db.get_or_404(Card, id)
    params = CardSchema().load(request.json, unknown='exclude')
    card.first_name = params.get('first_name', card.first_name)
    card.last_name = params.get('last_name', card.last_name)
    card.team_name = params.get('team_name', card.team_name)
    card.position = params.get('position', card.position)
    card.set = params.get('set', card.set)
    card.year = params.get('year', card.year)
    db.session.commit()
    return CardSchema().dump(card), 200
    

# Delete a card by its id (D)
@card_bp.route('/<int:id>', methods=['DELETE'])
@admin_only_search
def delete_card(id):
    # Queries the database for a card by its id, will 404 if not found
    card = db.get_or_404(Card, id)
    db.session.delete(card)
    db.session.commit()
    return {'message': 'Card deleted'}, 200
