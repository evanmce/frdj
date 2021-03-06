from app import app, db
from app.forms import LoginForm, RegistrationForm, AddFoodForm, RecipeSearchForm, ContactForm, SettingsForm
from app.models import User, Food, Recipe, FoodItem, ShoppingList
from flask import render_template, redirect, url_for, flash, jsonify, Response, request
from flask_login import current_user, login_user, logout_user, login_required
import sys
import json
from py_edamam import Edamam, PyEdamam
import requests

app_id = '9a9a5957'
app_key = '61b6cec1a891846e2d03c6f53aecaeb2'

#   ---------------------------------------------------------------------
#   Home / About / Contact
#   ---------------------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = AddFoodForm()
    if form.validate_on_submit():
        food = Food(name=form.name.data, food_type=form.food_type.data, user_id=current_user.id)
        db.session.add(food)
        db.session.commit()
        flash('{} added to your FRDJ'.format(form.name.data))
        return redirect(url_for('index'))
    foods = User.query.filter_by(username=current_user.username).first().get_food_list_by_type()
    return render_template('index.html', title='Home', form=form, foods=foods)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    return render_template('contact.html', title='Contact', form=form)

#   ---------------------------------------------------------------------
#   Recipes / Shopping List / Settings
#   ---------------------------------------------------------------------

@app.route('/recipe', methods=['GET', 'POST'])
@login_required
def recipe():
    form = RecipeSearchForm(valid_user_id=current_user.username)
    user = User.query.filter_by(username=current_user.username).first()
    food_list = user.foods.all()
    form.query_text.choices = [(f.name, f.name) for f in food_list]
    form.diet.choices = [('balanced', 'Balanced'), ('high protein', 'High Protein'), ('low-fat', 'Low Fat'), 
    ('low-carb', 'Low Carb'), ('vegan', 'Vegan'), ('vegetarian', 'Vegetarian'), ('sugar-conscious', 'Sugar Conscious'),
    ('peanut-free', 'Peanut Free'), ('tree-nut-free', 'Tree Nut Free'), ('alcohol-free', 'Alcohol Free')]
    if form.validate_on_submit():
        r = requests.get(
            'https://api.edamam.com/search?q={}&app_id={}&app_key={}&from=0&to={}&ingr={}&diet={}'.format(
                form.query_text.data, app_id, app_key, form.num_recipes.data, form.num_ingredients.data, form.diet.data))     
        recipes = json.loads(r.text)
        return render_template('recipe.html', title='Recipes Found', recipes=recipes['hits'])
    return render_template('recipe.html', title='Recipe', form=form)

@app.route('/shopping_list', methods=['GET', 'POST', 'PUT'])
@login_required
def shopping_list():
    form = AddFoodForm()
    user = User.query.filter_by(username=current_user.username).first()
    shopping_list = user.shopping_list.first()
    if request.method == "PUT":
        list_item = FoodItem.query.filter_by(id=request.args.get('item_id')).first()
        db.session.delete(list_item)
        db.session.commit()
        return '200'
    elif request.method == "POST" and form.validate_on_submit():
        item_name = form.name.data
        item_type = form.food_type.data
        list_id = shopping_list.id
        food_item = FoodItem(name=item_name, food_type=item_type, shopping_list_id=list_id)
        db.session.add(food_item)
        db.session.commit()
        return jsonify({"item_id": food_item.id, "item_name": food_item.name})
    else:
        return render_template('shopping_list.html', title='Shopping List', form=form, shopping_list=shopping_list.items.all())

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    return render_template('settings.html', title='Settings', form=form)

#   ---------------------------------------------------------------------
#   Login / Authentication
#   ---------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)