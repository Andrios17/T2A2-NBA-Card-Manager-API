from flask import Blueprint, request, jsonify
from models.pc import PersonalCollection, PersonalCollectionSchema
from init import db, ma
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.card import Card, CardSchema
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_
from sqlalchemy.exc import DataError
from auth import admin_or_owner

pc_bp = Blueprint('pc', __name__, url_prefix='/personal_collection')

# Get all personal collection in the users database (R)
@pc_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_pc():
    identity = get_jwt_identity()
    # Will query the database using the identity of the user to see which entities in the personal_collection table matches the user
    stmt = db.select(PersonalCollection).where(PersonalCollection.user_id == identity)
    collection = db.session.scalars(stmt).all()
    if collection:
        return PersonalCollectionSchema(many=True, exclude=['card_id', 'user_id']).dump(collection), 200
    else:
        return {'message': 'You do not have any cards in your collection'}, 200


# Get personal collection of a specific user (R)
@pc_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_pc_of_user(user_id):
    # Queries the database for a user's personal collection by using the provided id in the parameters
    stmt = db.select(PersonalCollection).where(PersonalCollection.user_id == user_id)
    collection = db.session.scalars(stmt).all()
    if collection != []:
        return PersonalCollectionSchema(many=True, exclude=['id', 'user_id']).dump(collection), 201
    else:
        return {'message': 'This user does not have any cards in their collection'}, 404


# Add a card to the users personal collection (C)
@pc_bp.route('/', methods=['POST'])
@jwt_required()
def create_pc():
    params = PersonalCollectionSchema().load(request.json, unknown='exclude')
    # Will query the database to see if the provided card_id in the params matches a known card in the card table
    stmt = db.select(Card).where(Card.id == params['card_id'])
    card = db.session.scalar(stmt)
    if card:
        pc = PersonalCollection(
            user_id=get_jwt_identity(),
            card_id=params['card_id'],
        )
        db.session.add(pc)
        db.session.commit()
        return PersonalCollectionSchema().dump(pc), 201
    else:
        return {'Error': 'Card does not exist'}, 404

# There is no update method for this blueprint as it would be redundant, it would be more beneficial for the user to just delete the entry and add a new one (U)

# Remove a card from the users personal collection (D)
@pc_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_pc(id):
    # Will ensure that the personal collection which is being deleted actually exists within the database.
    pc = db.get_or_404(PersonalCollection, id)
    admin_or_owner(pc)
    db.session.delete(pc)
    db.session.commit()
    return {'message': 'Card deleted from collection'}, 200

@pc_bp.errorhandler(DataError)
def ints_only(err):
    return {'error': 'please ensure you using ints when entering card_id'}, 404