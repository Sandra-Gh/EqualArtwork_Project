"""
This file contains the declarations of the models.
"""

from dataclasses import dataclass
from artwork import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


db.metadata.clear()


@dataclass  # dataclass is used to allow for converting objects to JSON in the webservice
class User(db.Model, UserMixin):

    id: int
    username: str
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='IMG_8912.JPG')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"<User(id='{self.id}', username='{self.username}', email='{self.email}', image_file='{self.image_file}')>"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.TEXT, nullable=True)

    def __repr__(self):
        return f"<Category(id='{self.id}', name='{self.name}', description='{self.description})'>"


class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(60), nullable=False)
    base = db.Column(db.Integer, nullable=False)
    color = db.Column(db.Integer, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    frame = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='IMG_8912.JPG')


    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, backref=db.backref('artworks', lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship(Category, backref=db.backref('artworks', lazy=True))

    def __repr__(self):
        return f"<Artwork(id='{self.id}', name='{self.name}', base='{self.base}', image_file='{self.image_file}," \
               f"color='{self.color}', date_posted='{self.date_posted}', size='{self.size}', frame='{self.frame}', time='{self.time}'," \
               f"user_id='{self.user_id}', category_id='{self.category_id}')>"

    def generate_price(self):
        price = 0

        if self.category.name == 'Abstract':
            a = 1
            while a <= self.size:
                price += a*50
                a += 1

            b = 1
            while b <= self.time:
                if self.time > 10 and self.time < 15:
                    price += 150
                    b += 1
                elif self.time < 20 and self.time > 15:
                    price += 100
                    b += 1
                elif self.time > 20:
                    price += 30
                    b += 1
                else:
                    price += 200
                    b += 1

            c = 1
            while c <= self.color:
                price += 100
                c += 1

            d = self.base
            if d == 1:
                if self.size == 1:
                    price = 100
                elif self.size == 2:
                    price = 200
                elif self.size == 3:
                    price = 350
                elif self.size == 4:
                    price = 450
                elif self.size == 5:
                    price = 550

            elif d == 2:
                price = price
            else:
                price += self.size * 20

            if self.frame != 1:
                price += 100

        elif self.category.name == 'Realistic':
            a = 1
            while a <= self.size:
                price += a * 100
                a += 1

            b = 1
            while b <= self.time:
                if self.time > 10 and self.time < 15:
                    price += 150
                    b += 1
                elif self.time < 20 and self.time > 15:
                    price += 100
                    b += 1
                elif self.time > 20:
                    price += 30
                    b += 1
                else:
                    price += 200
                    b += 1

            c = 1
            while c <= self.color:
                price += 100
                c += 1

            d = self.base
            if d == 1:
                if self.size == 1:
                    price = 100
                elif self.size == 2:
                    price = 200
                elif self.size == 3:
                    price = 350
                elif self.size == 4:
                    price = 450
                elif self.size == 5:
                    price = 550
            elif d == 2:
                price = price
            else:
                price += self.size * 20

            if self.frame != 1:
                price += 100

        elif self.category.name == 'Portrait':
            a = 1
            while a <= self.size:
                price += a * 300
                a += 1

            b = 1

            while b <= self.time:
                if self.time > 10 and self.time < 15:
                    price += 150
                    b += 1
                elif self.time < 20 and self.time > 15:
                    price += 100
                    b += 1
                elif self.time > 20:
                    price += 30
                    b += 1
                else:
                    price += 200
                    b += 1

            c = 1
            while c <= self.color:
                price += 100
                c += 1

            d = self.base
            if d == 1:
                if self.size == 1:
                    price = 100
                elif self.size == 2:
                    price = 200
                elif self.size == 3:
                    price = 350
                elif self.size == 4:
                    price = 450
                elif self.size == 5:
                    price = 550
            elif d == 2:
                price = price
            else:
                price += self.size * 20

            if self.frame != 1:
                price += 100
        return price


class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    bid_price = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, backref=db.backref('bids', lazy=True))

    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)
    artwork = db.relationship(Artwork, backref=db.backref('bids', lazy=True))

    def __repr__(self):
        return f"<Bid(id='{self.id}', bid_price='{self.bid_price}', user_id='{self.user_id}', artwork_id='{self.artwork_id}')>"









