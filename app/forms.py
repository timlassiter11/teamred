import pytz
from flask_wtf import FlaskForm
from wtforms import (BooleanField, EmailField, HiddenField, PasswordField,
                     SelectField, StringField, SubmitField, IntegerField, TimeField, FloatField)
from wtforms.validators import EqualTo, InputRequired, Length, NumberRange, ValidationError
from app.fields import TypeaheadField

from app.models import Airplane, Airport


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


class MethodForm(FlaskForm):
    """Form with a hidden field containing the form method.
    Used for handling method types not supported by standard 
    browsers such as DELETE and PUT.
    """
    method = HiddenField(default='POST')

    def validate(self, extra_validators=None):
        if self.method.data == 'DELETE':
            return self.csrf_token.validate(self)
        return super().validate(extra_validators=extra_validators)


class UserEditForm(MethodForm):
    email = EmailField('Email', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])


class AdminUserEditForm(UserEditForm):
    role = SelectField(
        'Role', choices=[('user', 'User'), ('agent', 'Agent'), ('admin', 'Admin')])


class AirportForm(FlaskForm):
    code = StringField('Code', validators=[
                       InputRequired(), Length(min=3, max=3)])
    name = StringField('Name', validators=[InputRequired()])
    timezone = SelectField('Timezone', choices=[(
        tz, tz) for tz in pytz.common_timezones])
    latitude = FloatField('Latitude', validators=[InputRequired()])
    longitude = FloatField('Longitude', validators=[InputRequired()])


class AirplaneForm(FlaskForm):
    registration_number = StringField('Registration Number', validators=[InputRequired()])
    model_name = StringField('Model Name', validators=[InputRequired()])
    model_code = StringField('Model Code', validators=[InputRequired()])
    capacity = IntegerField('Capacity', validators=[InputRequired(), NumberRange(min=0)])
    range = IntegerField('Range', validators=[InputRequired(), NumberRange(min=0)])
    home_code = TypeaheadField('Home Airport', validators=[InputRequired()])

    def _validate_airport(self, code):
        airport = Airport.query.filter_by(code=code).first()
        if not airport:
            raise ValidationError('No airport with that code exists')
        return airport

    def validate_home_code(form, field):
        airport = form._validate_airport(field.data)
        form.home_id = airport.id





class FlightForm(FlaskForm):
    number = StringField('Flight Number', validators=[InputRequired(), Length(min=1, max=4)])
    airplane_registration = TypeaheadField('Plane', validators=[InputRequired()])
    departing_code = TypeaheadField('Departing From', validators=[InputRequired(), Length(min=3, max=3)])
    arriving_code = TypeaheadField('Arriving To', validators=[InputRequired(), Length(min=3, max=3)])
    departure_time = TimeField('Departing Time', validators=[InputRequired()], format='%H:%M:%S')
    arrival_time = TimeField('Arriving Time', validators=[InputRequired()], format='%H:%M:%S')
    cost = FloatField('Cost', validators=[InputRequired()])

    def validate_airplane_registration(form, field):
        airplane = Airplane.query.filter_by(registration_number=field.data).first()
        if not airplane:
            raise ValidationError('No plane with that registration number exists')
        form.airplane_id = airplane.id

    def _validate_airport(self, code):
        airport = Airport.query.filter_by(code=code).first()
        if not airport:
            raise ValidationError('No airport with that code exists')
        return airport

    def validate_departing_code(form, field):
        airport = form._validate_airport(field.data)
        form.departing_id = airport.id

    def validate_arriving_code(form, field):
        airport = form._validate_airport(field.data)
        form.arriving_id = airport.id
