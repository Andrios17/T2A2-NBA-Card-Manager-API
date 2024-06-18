from flask import Blueprint
from models.card import Card
from models.user import User
from models.post import Post
from models.pc import PersonalCollection
from init import db, bcrypt

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def db_create():
    db.drop_all()
    db.create_all()
    print('Created all tables')

@db_commands.cli.command('seed_users')
def seed_users():
    users = [
        User(
            username='Administrator',
            email='admin@fake.com',
            password= bcrypt.generate_password_hash("Knicks123").decode('utf8'),
            first_name='Head',
            last_name='Admin',
            is_admin=True,
        ),
        User(
            username='User',
            email='user@fake.com',
            password= bcrypt.generate_password_hash("Julius_Randle").decode('utf8'),
            first_name='Number',
            last_name='One',
            is_admin=False,
        )
    ]

    db.session.add_all(users)
    db.session.commit()
    print('Seeded Users')
