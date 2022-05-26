from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import EqualTo, InputRequired


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    password2 = PasswordField('Confirm Password', validators=[
                              InputRequired(), EqualTo('password', message='Passwords do not match')])
    submit = SubmitField('Register')


class ResetPasswordRequestForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    submit = SubmitField('Request')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])
    password2 = PasswordField('Confirm Password', validators=[
                              InputRequired(), EqualTo('password', message='Passwords do not match')])
    submit = SubmitField('Reset Password')
