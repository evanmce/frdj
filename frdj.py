from app import app, db
from app.models import User, Food, Recipe, FoodItem, ShoppingList
from app.routes import app_id, app_key
from py_edamam import PyEdamam, Edamam

import requests
import json

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Food': Food, 'app_id': app_id, 'app_key': app_key, 'PyEdamam': PyEdamam,
            'ShoppingList': ShoppingList, 'FoodItem': FoodItem}