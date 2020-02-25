from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, Form, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, NumberRange
from app.models import User, Food, FoodTypes

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')

class AddFoodForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    food_type = SelectField('Food Type', choices=FoodTypes)
    submit = SubmitField('Add Food')

class RecipeSearchForm(FlaskForm):
    query_text = SelectField('Food', validators=[DataRequired()], id='select_query')
    num_recipes = IntegerField('Number of Recipes', validators=[DataRequired(), NumberRange(min=0, max=20)], default=1)
    num_ingredients = IntegerField('Max Number of Ingredients', validators=[DataRequired(), NumberRange(min=5, max=25)], default=10)
    diet = SelectField('Diet / Allergies', id='select_diet')
    submit = SubmitField('Search Recipe')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Contact Us')

class SettingsForm(FlaskForm):
    name = StringField('Name')
    