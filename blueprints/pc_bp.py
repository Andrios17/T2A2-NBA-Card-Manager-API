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

@pc_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_pc():
    identity = get_jwt_identity()
    stmt = db.select(PersonalCollection).where(PersonalCollection.user_id == identity)
    collection = db.session.scalars(stmt).all()
    if collection:
        return PersonalCollectionSchema(many=True, exclude=['card_id', 'user_id']).dump(collection), 201
    else:
        return {'message': 'You do not have any cards in your collection'}, 200

@pc_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_pc_of_user(user_id):
    stmt = db.select(PersonalCollection).where(PersonalCollection.user_id == user_id)
    collection = db.session.scalars(stmt).all()
    if collection != []:
        return PersonalCollectionSchema(many=True, exclude=['id', 'user_id']).dump(collection), 201
    else:
        return {'message': 'This user does not have any cards in their collection'}, 404

@pc_bp.route('/', methods=['POST'])
@jwt_required()
def create_pc():
    params = PersonalCollectionSchema().load(request.json, unknown='exclude')
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
        return {'message': 'Card does not exit'}, 404

@pc_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_pc(id):
    pc = db.get_or_404(PersonalCollection, id)
    admin_or_owner(pc)
    db.session.delete(pc)
    db.session.commit()
    return {'message': 'Card deleted from collection'}, 200

@pc_bp.errorhandler(DataError)
def ints_only(err):
    return {'error': 'please ensure you using ints when entering card_id'}, 404