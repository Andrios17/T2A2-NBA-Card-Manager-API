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

@db_commands.cli.command('seed_tables')
def seed_tables():
    users = [
        User(
            username='Administrator',
            email='admin@fake.com',
            password= bcrypt.generate_password_hash("Whatupimtheadmin17").decode('utf8'),
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

    cards = [
        Card(
            first_name='Jalen',
            last_name='Brunson',
            team_name='New York Knicks',
            position='PG',
            set='Panini Prizm',
            year=2023
        ),
        Card(
            first_name='Lebron',
            last_name='James',
            team_name='Los Angleas Lakers',
            position='SF',
            set='Panini Prizm',
            year=2023
        ),
        Card(
            first_name='Klay',
            last_name='Thompson',
            team_name='Golden State Warriors',
            position='SG',
            set='Panini Prizm',
            year=2023
        ),
        Card(
            first_name='Stephen',
            last_name='Curry',
            team_name='Golden State Warriors',
            position='PG',
            set='Panini Prizm',
            year=2011
        ),
        Card(
            first_name='Kevin',
            last_name='Durant',
            team_name='Oklahoma City Thunder',
            position='SF',
            set='National Treasures',
            year=2018
        ),
        Card(
            first_name='Michael',
            last_name='Jordan',
            team_name='Chicago Bulls',
            position='SG',
            set='Fleer',
            year=1984
        ),
        Card(
            first_name='Kobe',
            last_name='Bryant',
            team_name='Los Angeles Lakers',
            position='SG',
            set='National Treasures',
            year=2016
        ),
        Card(
            first_name='LeBron',
            last_name='James',
            team_name='Cleveland Cavaliers',
            position='SF',
            set='National Treasures',
            year=2003
        ),
        Card(
            first_name='Julius',
            last_name='Randle',
            team_name='New York Knicks',
            position='PF',
            set='Panini Prizm',
            year=2020
        ),
        Card(
            first_name='Larry',
            last_name='Bird',
            team_name='Boston Celtics',
            position='SF',
            set='Fleer',
            year=1982
        )
    ]

    db.session.add_all(cards)
    db.session.commit()
    print('Seeded Cards')


    posts = [
        Post(
            title='First Post',
            description='This is my first post',
            date_posted=date.today(),
            user_id=1,
        ),
        Post(
            title='Second Post',
            description='This is my second post',
            date_posted=date.today(),
            user_id=2,
        )
    ]

    db.session.add_all(posts)
    db.session.commit()
    print('Seeded Posts')

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

    pcs = [
        PersonalCollection(
            card_id=1,
            user_id=1
        ),
        PersonalCollection(
            card_id=2,
            user_id=1
        )
    ]

    db.session.add_all(pcs)
    db.session.commit()
    print('Seeded Personal Collections')

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

    bids = [
        Bid(
            price=200,
            auction_id=1,
            user_id=2,
            date = date.today()
        ),
        Bid(
            price=200,
            auction_id=2,
            user_id=1,
            date = date.today()
        )
    ]

    db.session.add_all(bids)
    db.session.commit()
    print('Seeded Bids')
