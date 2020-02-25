from app import db, login
from datetime import datetime
import enum
from flask_login import UserMixin
from sqlalchemy import Integer, Enum
from werkzeug.security import generate_password_hash, check_password_hash

FoodTypes = [('Fruit', 'Fruit'), ('Vegetable', 'Vegetable'), ('Grain', 'Grain'), ('Meat', 'Meat'), ('Seafood', 'Seafood'), ('Dairy', 'Dairy'), ('Spice', 'Spice')]

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    foods = db.relationship('Food', backref='user', lazy='dynamic')
    recipes = db.relationship('Recipe', backref='user', lazy='dynamic')
    shopping_list = db.relationship('ShoppingList', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_food_list_by_type(self):
        food_types = []
        for f_type in FoodTypes:
            f = [food for food in self.foods if food.food_type==f_type[0]]
            food_types.append(f)
        return food_types

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Food(db.Model):
    __tablename__ = 'food'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    food_type = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Name: {} Type: {}>'.format(self.name, self.food_type)

    def __init__(self, name, food_type, user_id):
        self.name = name
        self.food_type = food_type
        self.user_id = user_id

class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

class FoodItem(db.Model):
    __tablename__ = 'food_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    food_type = db.Column(db.String(32))
    shopping_list_id = db.Column(db.Integer, db.ForeignKey('shopping_list.id'))

    def __init__(self, name, food_type, shopping_list_id):
        self.name = name
        self.food_type = food_type
        self.shopping_list_id = shopping_list_id

    def __repr__(self):
        return '<Name: {} Type: {}>'.format(self.name, self.food_type)

class ShoppingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('FoodItem', backref='shopping_list', lazy='dynamic')

    def __init__(self, user_id):
        self.user_id = user_id

