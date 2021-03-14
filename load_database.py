import os
import sys
import random
import datetime
import requests
from artwork import db, bcrypt
from artwork.models import User, Category, Artwork, Bid
from lorem_text import lorem


host = 'localhost'  # host where the system is running
port = 5000  # port where the process is running


def reload_database():
    exit_reload = False
    try:
        response = requests.get(f'http://{host}:{port}')
        print('The website seems to be running. Please stop it and run this file again.', file=sys.stderr)
        exit_reload = True
    except:
        pass
    if exit_reload:
        exit(11)
    try:
        os.remove('artwork/site.db')
        print('previous DB file removed')
    except:
        print('no previous file found')

    db.create_all()

    # creating two users
    hashed_password = bcrypt.generate_password_hash('testing').decode('utf-8')
    default_user1 = User(username='Default',
                         email='default@test.com',
                         image_file='another_pic.jpeg',
                         password=hashed_password)
    db.session.add(default_user1)

    hashed_password = bcrypt.generate_password_hash('testing2').decode('utf-8')
    default_user2 = User(username='Default Second',
                         email='second@test.com',
                         image_file='7798432669b8b3ac.jpg',
                         password=hashed_password)
    db.session.add(default_user2)

    hashed_password = bcrypt.generate_password_hash('testing3').decode('utf-8')
    default_user3 = User(username='Default Third',
                         email='third@test.com',
                         password=hashed_password)
    db.session.add(default_user3)

    # TODO: Here you should include the generation of rows for your database
    cat_1 = Category(name='Abstract')
    cat_2 = Category(name='Realistic')
    cat_3 = Category(name='Portrait')
    categories = [cat_1, cat_2, cat_3]
    db.session.add_all(categories)

    artworks = []

    for r in range(100):
        user = random.choice([default_user1, default_user2, default_user3])
        name = random.choice(lorem.sentence()) #shouldn't be a sentence but just for testing
        base = random.randint(1, 3)
        color = random.randint(0, 10)
        time = random.randint(1, 80)
        size = random.randint(1, 10)
        frame = random.randint(1, 2)
        image_file = 'IMG_8912.JPG'
        date_posted = datetime.datetime.now() - \
                      datetime.timedelta(days=random.randint(0, 160),
                                         hours=random.randint(0, 24),
                                         minutes=random.randint(0, 60))
        category = random.choice(categories)
        artwork = Artwork(user=user,
                          name=name,
                          base=base,
                          color=color,
                          time=time,
                          size=size,
                          frame=frame,
                          image_file=image_file,
                          date_posted=date_posted,
                          category=category
                          )
        p = artwork.generate_price()
        db.session.add(artwork)
        artworks.append(artwork)

    # price method in artwork will be implemented later


    for b in range(100):
        user = random.choice([default_user1, default_user2, default_user3])
        artwork = (random.choice(artworks))
        bid_price = random.randint(artwork.generate_price(), 700000)
        bid = Bid(bid_price=bid_price, user=user, artwork=artwork)
        db.session.add(bid)

    try:
        db.session.commit()
        print('\nFinalized - database created successfully!')
    except Exception as e:
        print('The operations were not successful. Error:', file=sys.stderr)
        print(e, file=sys.stderr)
        db.session.rollback()


if __name__ == '__main__':
    reload_database()
