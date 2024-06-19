from flask import Blueprint,request
from init import db, ma
from models.card import Card, CardSchema

card_bp = Blueprint('card', __name__, url_prefix='/cards')

@card_bp.route('/', methods=['GET'])
def get_all_cards():
    cards = db.session.query(Card).all()
    return CardSchema(many=True).dump(cards), 200

@card_bp.route('/<int:id>', methods=['GET'])
def get_card(id):
    card = db.session.query(Card).get(id)
    return CardSchema().dump(card), 200

@card_bp.route('/', methods=['POST'])
# @admin_required
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

@card_bp.route('/', methods=['PUT', 'PATCH'])
# @admin_required
def update_card():
    params = CardSchema().load(request.json, unknown='exclude')
    card = db.session.query(Card).get(params['id'])
    card.first_name = params['first_name']
    card.last_name = params['last_name']
    card.team_name = params['team_name']
    card.position = params['position']
    card.set = params['set']
    card.year = params['year']
    db.session.commit()
    return CardSchema().dump(card), 200

@card_bp.route('/<int:id>', methods=['DELETE'])
# @admin_required
def delete_card(id):
    card = db.session.query(Card).get(id)
    db.session.delete(card)
    db.session.commit()
    return {'message': 'Card deleted'}, 200
