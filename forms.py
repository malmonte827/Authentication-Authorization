from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class RegisterForm(FlaskForm):
    """ Create New User """
    username = StringField('Username', validators=[InputRequired(), Length(max = 20, message="Username can't be longer than 20 characters")])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(),Email(), Length(max=50, message= "Email can't be longer than 50 characters")])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30, message= "First name can't be longer than 30 characters")])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30, message= "Last name can't be longer than 30 characters")])