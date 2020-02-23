from app import db, login
from datetime import datetime
import enum
from flask_login import UserMixin
from sqlalchemy import Integer, Enum
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    foods = db.relationship('Food', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# class FoodTypes(enum.Enum):
#     Vegetable = 1
#     Fruit = 2
#     Grain = 3
#     Meat = 4
#     Seafood = 5
#     Dairy = 6
#     Spice = 7

FoodTypes = [('Vegetable', 'Vegetable'), ('Fruit', 'Fruit'), ('Grain', 'Grain'), ('Meat', 'Meat'), ('Seafood', 'Seafood'), ('Dairy', 'Dairy'), ('Spice', 'Spice')]

class Food(db.Model):
    __tablename__ = 'food'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    # food_type = db.Column(Enum(FoodTypes))
    food_type = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Name: {}\nType: {}>'.format(self.name, self.food_type)

    def __init__(self, name, food_type):
        self.name = name
        self.food_type = food_type

