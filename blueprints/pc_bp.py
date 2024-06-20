from flask import Blueprint
from models.pc import PersonalCollection, PersonalCollectionSchema


pc_bp = Blueprint('pc', __name__, url_prefix='\personal_collection')

@pc_bp.route('/', methods=['GET'])
def get_all_pc():
    pass

@pc_bp.route('/<int:id>', methods=['GET'])
def get_pc(id):
    pass

@pc_bp.route('/', methods=['POST'])
def create_pc():
    pass

@pc_bp.route('/', methods=['PUT', 'PATCH'])
def update_pc():
    pass

@pc_bp.route('/<int:id>', methods=['DELETE'])
def delete_pc(id):
    pass

