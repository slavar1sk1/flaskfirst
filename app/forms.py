from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField, PasswordField, BooleanField
from flask_wtf.file import FileRequired
from wtforms.validators import DataRequired, EqualTo


class Form(FlaskForm):
    title = StringField(label='Title:', validators=[DataRequired()])
    intro = StringField(label='Intro:', validators=[DataRequired()])
    text = StringField(label='Text:', validators=[DataRequired()])
    catalog = SelectField(label='Catalog:', choices=[('option1', 'Игры'), ('option2', 'Программирование')],
                          validators=[DataRequired()])
    price = StringField(label='Price (in Euro):', validators=[DataRequired()])
    img = FileField(label='Image:', validators=[FileRequired()])
    submit = SubmitField(label='Submit')


class Login(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember me')
    login = SubmitField(label='Login')


class Registration(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm password:', validators=[DataRequired(), EqualTo('password')])
    email = StringField(label='Email:', validators=[DataRequired()])
    registration = SubmitField(label='Registration')