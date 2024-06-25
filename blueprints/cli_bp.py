from datetime import date, timedelta
from flask import Blueprint
from models.card import Card
from models.user import User
from models.post import Post
from models.pc import PersonalCollection
from models.comment import Comment
from models.auction import Auction
from models.bid import Bid
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
            password= bcrypt.generate_password_hash("/10").decode('utf8'),
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

@db_commands.cli.command('seed_cards')
def seed_cards():
    cards = [
        Card(
            first_name='Jalen',
            last_name='Brunson',
            team_name='New York Knicks',
            position='PG',
            set='Panini Prizm 2023-24',
            year=2023
        ),
        Card(
            first_name='Lebron',
            last_name='James',
            team_name='Los Angleas Lakers',
            position='SF',
            set='Panini Prizm 2023-24',
            year=2023
        )
    ]

    db.session.add_all(cards)
    db.session.commit()
    print('Seeded Cards')

@db_commands.cli.command('seed_posts')
def seed_posts():
    posts = [
        Post(
            title='First Post',
            description='This is my first post',
            date_posted=date.today(),
            user_id=1,
            user_username='Administrator'
        ),
        Post(
            title='Second Post',
            description='This is my second post',
            date_posted=date.today(),
            user_id=2,
            user_username='User'
        )
    ]

    db.session.add_all(posts)
    db.session.commit()
    print('Seeded Posts')

@db_commands.cli.command('seed_comments')
def seed_comments():
    comments = [
        Comment(
        message='This is a comment',
        date_posted=date.today(),
        post_id=1,
        user_id=1
        ),
    Comment(
        message='This is another comment',
        date_posted=date.today(),
        post_id=1,
        user_id=2
        )
    ]

    db.session.add_all(comments)
    db.session.commit()
    print('Seeded Comments')

@db_commands.cli.command('seed_auctions')
def seed_auctions():
    auctions = [
        Auction(
            start_date=date.today(),
            end_date=date.today() + timedelta(weeks=1),
            start_price=100,
            card_id=1,
            user_id=1
        ),
        Auction(
            start_date=date.today(),
            end_date=date.today() + timedelta(weeks=1),
            start_price=100,
            card_id=2,
            user_id=1,
        )
    ]

    db.session.add_all(auctions)
    db.session.commit()
    print('Seeded Auctions')

@db_commands.cli.command('seed_bids')
def seed_bids():
    # bids = [
    #     Bid(
    #         price=100,
    #         auction_id=3,
    #         user_id=1,
    #         date = date.today()
    #     ),
    #     Bid(
    #         price=100,
    #         auction_id=4,
    #         user_id=2,
    #         date = date.today()
    #     )
    # ]

    bids = [
        Bid(
            price=200,
            auction_id=3,
            user_id=2,
            date = date.today()
        ),
        Bid(
            price=200,
            auction_id=4,
            user_id=1,
            date = date.today()
        )
    ]

    db.session.add_all(bids)
    db.session.commit()
    print('Seeded Bids')
